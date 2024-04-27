from multiprocessing import context
from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ServiceRequest
from .models import GasCustomer
from django.contrib import messages
from .models import User, GasCustomer
from django.shortcuts import redirect


def submit_request_view(request):
    if request.method == 'POST':
        request_type = request.POST.get('request_type')
        details = request.POST.get('details')
        attachment = request.FILES.get('attachment')

        new_request = ServiceRequest(request_type=request_type, details=details, attachment=attachment)
        new_request.save()

        messages.success(request, 'Service request submitted successfully!')

        return redirect('track_request')

    return render(request, 'submit_request.html')

def track_request(request):
    service_requests = ServiceRequest.objects.filter(user=request.user)
    return render(request, 'track_request.html', {'service_requests': service_requests})

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return redirect('submit_request')
        else:
            error_message = "Invalid credentials. Please try again."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request, 'login.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('upass')
        confirm_password = request.POST.get('ucpass')
        customer_id = request.POST.get('customer_id')

        if User.objects.filter(username=username).exists():
            error_message = "Username already exists. Please choose a different one."
            return render(request, 'register.html', {'errormsg': error_message})
    
        if GasCustomer.objects.filter(customer_id=customer_id).exists():
            error_message = "Customer ID already exists. Please choose a different one."
            return render(request, 'register.html', {'errormsg': error_message})


        if password != confirm_password:
            error_message = "Passwords do not match. Please try again."
            return render(request, 'register.html', {'errormsg': error_message})

        try:
            user = User.objects.create_user(username=username, password=password)

            customer = GasCustomer.objects.create(customer_id=customer_id, user=user)

            success_message = "Registration successful. You can now login."
            return render(request, 'register.html', {'success': success_message})
        except Exception as e:
            # Catch any exceptions that might occur during user or customer creation
            error_message = f"An error occurred: {str(e)}"
            return render(request, 'register.html', {'errormsg': error_message})

    # If the request method is not POST, render the registration form
    return render(request, 'register.html')