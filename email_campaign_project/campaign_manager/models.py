from django.db import models
from django.utils import timezone

class Subscriber(models.Model):
    email = models.EmailField(unique=True , db_index=True)
    first_name = models.CharField(max_length=100 , blank=True , null=True)
    is_active = models.BooleanField(default=True , db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.email
    
    
    
class Campaign(models.Model):
    subject = models.CharField(max_length=250)
    preview_text = models.CharField(max_length=250 , blank=True , null=True)
    artical_url = models.URLField(blank=True , null=True)
    html_content = models.TextField(help_text="Main HTML body of the email. Variable like {{first_name}},{{unsubscriber_url}} can be used.")
    plain_text_content = models.TextField(help_text="Plain text version . Variables like {{first_name}} , {{unsubscribe_url}} can be used.") 
    published_date = models.DateField(default=timezone.now , db_index=True)
    is_sent = models.BooleanField(default=False , db_index=True)
    send_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.subject
