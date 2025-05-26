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

def profile_view(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')  # Refreshes the page
    return render(request, 'users/profile.html', {
        'form': form,
    })





