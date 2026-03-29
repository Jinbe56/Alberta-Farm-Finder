from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
        return redirect('farms:search')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            is_farmer = request.POST.get('account_type') == 'farmer'
            UserProfile.objects.create(user=user, is_farmer=is_farmer)
            login(request, user)
            if is_farmer:
                messages.success(request, 'Welcome! Let\'s get your farm listed.')
                return redirect('farms:create')
            else:
                messages.success(request, 'Welcome to Farm Finder!')
                return redirect('farms:search')
    else:
        form = UserCreationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('farms:search')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html')


def logout_view(request):
    logout(request)
    return redirect('farms:search')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile.display_name = request.POST.get('display_name', '').strip()
        profile.save()
        request.user.email = request.POST.get('email', '').strip()
        request.user.save()
        messages.success(request, 'Profile updated!')
        return redirect('accounts:profile')

    return render(request, 'accounts/profile.html', {'profile': profile})
