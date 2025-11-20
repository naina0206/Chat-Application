from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from .models import Message
from .forms import CustomUserCreationForm, LoginForm

def signup_view(request):
    """User registration view"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'chat/signup.html', {'form': form})

def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('chat')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('chat')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            # Show specific form errors
            if form.errors:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, f'{field}: {error}')
            else:
                messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()
    
    return render(request, 'chat/login.html', {'form': form})

def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

@login_required
def chat_view(request):
    """Render the chat interface - requires login"""
    # Get all users except the current user
    other_users = User.objects.exclude(id=request.user.id)
    return render(request, 'chat/index.html', {'other_users': other_users})

def get_message_history(request, username1, username2):
    """Get chat history between two users"""
    # Get all messages between these two users
    messages = Message.objects.filter(
        Q(sender__username=username1, receiver__username=username2) |
        Q(sender__username=username2, receiver__username=username1)
    ).select_related('sender', 'receiver').order_by('timestamp')
    
    # Convert to JSON format
    message_list = [{
        'sender': msg.sender.username,
        'receiver': msg.receiver.username,
        'message': msg.content,
        'timestamp': msg.timestamp.isoformat()
    } for msg in messages]
    
    return JsonResponse({'messages': message_list})