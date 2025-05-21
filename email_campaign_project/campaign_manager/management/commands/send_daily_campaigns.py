from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from campaign_manager.models import Campaign, Subscriber
from campaign_manager.email_utils import send_campaign_to_subscriber
import concurrent.futures
import time

# Define a sensible number of threads. Too many can overwhelm SMTP or local resources.
MAX_WORKERS = getattr(settings, 'EMAIL_MAX_WORKERS', 5)

class Command(BaseCommand):
    help = 'Sends daily email campaigns that are due and not yet sent.'

    def send_single_email_task(self, campaign_id, subscriber_id):
        """ Helper function to be run in a thread """
        try:
            campaign = Campaign.objects.get(id=campaign_id)
            subscriber = Subscriber.objects.get(id=subscriber_id)
            # The actual sending logic
            send_campaign_to_subscriber(campaign, subscriber)
            return f"Successfully sent to {subscriber.email}"
        except Campaign.DoesNotExist:
            return f"Campaign {campaign_id} not found for subscriber {subscriber_id}"
        except Subscriber.DoesNotExist:
            return f"Subscriber {subscriber_id} not found for campaign {campaign_id}"
        except Exception as e:
            return f"Error sending to subscriber {subscriber_id} for campaign {campaign_id}: {e}"

    def handle(self, *args, **options):
        today = timezone.now().date()
        # Campaigns scheduled for today (or earlier and missed) that haven't been sent
        campaigns_to_send = Campaign.objects.filter(
            published_date__lte=today,
            is_sent=False
        )

        if not campaigns_to_send.exists():
            self.stdout.write(self.style.SUCCESS('No campaigns to send today.'))
            return

        active_subscribers = list(Subscriber.objects.filter(is_active=True))  # Fetch once

        if not active_subscribers:
            self.stdout.write(self.style.WARNING('No active subscribers to send emails to.'))
            return

        for campaign in campaigns_to_send:
            self.stdout.write("\n=== Campaign Details ===")
            for field in Campaign._meta.fields:
                value = getattr(campaign, field.name)
                self.stdout.write(f"{field.name}: {value}")

            start_time = time.time()
            emails_sent_count = 0
            emails_failed_count = 0

            # Using ThreadPoolExecutor for parallel dispatching
            with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
                # Create a list of future tasks
                future_to_subscriber = {
                    executor.submit(self.send_single_email_task, campaign.id, subscriber.id): subscriber
                    for subscriber in active_subscribers
                }

                for future in concurrent.futures.as_completed(future_to_subscriber):
                    subscriber = future_to_subscriber[future]
                    try:
                        result_message = future.result()  # Get result or exception
                        if "Successfully sent" in result_message:
                            emails_sent_count += 1
                            self.stdout.write(self.style.SUCCESS(f"  {result_message}"))
                        else:
                            emails_failed_count += 1
                            self.stdout.write(self.style.ERROR(f"  {result_message}"))
                    except Exception as exc:
                        emails_failed_count += 1
                        self.stdout.write(self.style.ERROR(f'  Email to {subscriber.email} generated an exception: {exc}'))

            end_time = time.time()
            total_time = end_time - start_time

            # Mark campaign as sent after attempting all subscribers
            campaign.is_sent = True
            campaign.sent_at = timezone.now()
            campaign.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Finished campaign '{campaign.subject}'. "
                    f"Sent: {emails_sent_count}, Failed: {emails_failed_count}. "
                    f"Time taken: {total_time:.2f} seconds."
                )
            )

        self.stdout.write(self.style.SUCCESS('All due campaigns processed.'))
