from django.urls import path
from . import views

urlpatterns = [
    path('api/subscribe/', views.add_subscriber_api, name='api_add_subscriber'),
    path('unsubscribe/', views.unsubscribe_user, name='unsubscribe'),
    path('add-subscriber-form/', views.add_subscriber_view, name='add_subscriber_form'), # HTML form endpoint
    
]