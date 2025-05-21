


from django.http  import HttpResponse
from django.shortcuts import render

def home(request):
  #  return HttpResponse("Hello, world. You're at the chaiaurDjango home page.")
    return render(request , 'website/index.html')
      
def about(request):
    return HttpResponse("This is the about page.")

def contact(request):
    return HttpResponse("This is the contact page.")
