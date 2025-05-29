from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required


from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # this triggers the signal to create the Profile
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})




def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect('home')  # Make sure you have a 'home' route
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid credentials.")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})




def logout_view(request):
    logout(request)
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('dashboard')  # or your homepage
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})



from django.shortcuts import render, redirect
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth.decorators import login_required

from django.contrib import messages

import random
from django.core.mail import send_mail
from django.conf import settings

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.core.mail import send_mail
from django.conf import settings
import random

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm
from django.core.mail import send_mail
from django.conf import settings
import random

@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile, user=user)
        verification_code_input = request.POST.get('verification_code')
        stored_code = request.session.get('verification_code')
        email_pending = request.session.get('pending_email')

        # Handle email verification
        if verification_code_input:
            if verification_code_input == stored_code:
                profile.notify_email = email_pending
                profile.save()
                messages.success(request, "Email verified and saved.")
                request.session.pop('verification_code', None)
                request.session.pop('pending_email', None)
                return redirect('profile')  # Redirect to dashboard if verification is successful
            else:
                messages.error(request, "Invalid verification code.")
        else:
            # Handle profile form submission
            if form.is_valid():
                form.save()  # Save the profile

                # Check if the profile is complete after updating
                if profile.is_complete():
                    messages.success(request, "Profile updated successfully.")
                    return redirect('dashboard')  # Redirect to dashboard if profile is complete
                else:
                    messages.warning(request, "Please complete your profile.")

                # Send verification code if notify_email is updated
                new_email = form.cleaned_data['notify_email']
                code = str(random.randint(100000, 999999))
                request.session['verification_code'] = code
                request.session['pending_email'] = new_email

                send_mail(
                    subject='Your FitNotify Verification Code',
                    message=f'Your code is: {code}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[new_email],
                    fail_silently=False
                )

                messages.info(request, "Verification code sent to your email. Please enter it below.")
                return redirect('profile')  # Redirect to profile after sending verification code

    else:
        form = ProfileForm(instance=profile, user=user)

    needs_verification = request.session.get('verification_code') is not None

    return render(request, 'users/profile.html', {
        'form': form,
        'needs_verification': needs_verification,
    })




