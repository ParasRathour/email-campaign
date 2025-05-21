from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.urls import reverse
import logging

logger = logging.getLogger(__name__)

def send_campaign_to_subscriber(campaign, subscriber):
    """
    Sends a single campaign email to a single subscriber.
    """
    # Generate unsubscribe URL (ensure your site domain is configured in settings.SITE_ID or build it manually)
    # For simplicity, assuming http and localhost. In production, use settings.SITE_DOMAIN or request object.
    unsubscribe_path = reverse('unsubscribe')
    # This is a basic way, for production consider settings.SITE_URL or similar
    unsubscribe_url = f"http://127.0.0.1:8000{unsubscribe_path}" 

    context = {
        'subject': campaign.subject,
        'preview_text': campaign.preview_text,
        'article_url': campaign.artical_url,
        'campaign_html_content': campaign.html_content, # Pass the campaign's specific HTML
        'campaign_plain_text_content': campaign.plain_text_content, # Pass the campaign's specific plain text
        'first_name': subscriber.first_name,
        'unsubscribe_url': unsubscribe_url,
    }

    # Render from base templates, injecting campaign-specific content
    html_body = render_to_string('campaign_manager/base_email.html', context)
    text_body = render_to_string('campaign_manager/base_email.txt', context)

    try:
        msg = EmailMultiAlternatives(
            subject=campaign.subject,
            body=text_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber.email]
        )
        msg.attach_alternative(html_body, "text/html")
        msg.send()
        logger.info(f"Email sent to {subscriber.email} for campaign '{campaign.subject}'")
        return True
    except Exception as e:
        logger.error(f"Failed to send email to {subscriber.email} for campaign '{campaign.subject}': {e}")
        return False