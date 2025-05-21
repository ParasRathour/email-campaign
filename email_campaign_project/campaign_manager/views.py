from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt 
import json

from .models import Subscriber
from .forms import SubscriberForm

# Endpoint to Add Subscribers 
@csrf_exempt 
@require_POST
def add_subscriber_api(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        first_name = data.get('first_name')

        if not email:
            return JsonResponse({'status': 'error', 'message': 'Email is required.'}, status=400)

        subscriber, created = Subscriber.objects.get_or_create(
            email=email,
            defaults={'first_name': first_name, 'is_active': True}
        )

        if not created: # If subscriber existed
            if not subscriber.is_active:
                subscriber.is_active = True # Reactivate if inactive
                subscriber.first_name = first_name if first_name else subscriber.first_name
                subscriber.save()
                return JsonResponse({'status': 'success', 'message': 'Subscriber reactivated.'})
            return JsonResponse({'status': 'info', 'message': 'Subscriber already exists and is active.'})
        
        return JsonResponse({'status': 'success', 'message': 'Subscriber added.'}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'Invalid JSON.'}, status=400)
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

# Endpoint to unsubscribe users
def unsubscribe_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
           subscriber = get_object_or_404(Subscriber, email=email)
           subscriber.is_active = False
           subscriber.save()
           return render(request, 'campaign_manager/unsubscribe_success.html', {'email': email})
        except Subscriber.DoesNotExist:
           return HttpResponse(f"Subscriber with email {email} not found.", status=404)
        
    return render(request, 'campaign_manager/get_email.html')

# HTML page to add subscribers 
def add_subscriber_view(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            first_name = form.cleaned_data['first_name']
            subscriber, created = Subscriber.objects.get_or_create(
                email=email,
                defaults={'first_name': first_name, 'is_active': True}
            )    
            if not created and not subscriber.is_active:
                subscriber.is_active = True
                subscriber.first_name = first_name if first_name else subscriber.first_name
                subscriber.save()
            return redirect('add_subscriber_form') 
    else:
        form = SubscriberForm()
    return render(request, 'campaign_manager/add_subscriber_form.html', {'form': form})