from django.contrib import admin
from .models import Subscriber , Campaign

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'is_active', 'created_at', 'updated_at')
    list_filter = ('is_active' , 'created_at')
    search_fields = ('email' , 'first_name')
    actions = ['mark_active' , 'mark_inactive']
    
    def mark_active(self , request , queryset):
        queryset.update(is_active=True)
    mark_active.short_description = "Mark selected subscribers as active"  
      
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)
    mark_inactive.short_description = "Mark selected subscribers as inactive"  


@admin.register(Campaign)
class CampaignAdmin(admin.ModelAdmin):
    list_display = ('subject', 'published_date', 'is_sent', 'send_at', 'update_at')
    list_filter = ('is_sent', 'published_date')
    search_fields = ('subject', 'preview_text')
    ordering = ('-published_date',)