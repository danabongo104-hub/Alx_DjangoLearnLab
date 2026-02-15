from django.shortcuts import render,redirect
from .models import Post
from .forms import CustomUserCreationForm,ProfileUpdateForm,UserUpdateForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login
from django.contrib import messages


# Create your views here.

def registerPage(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        print("Form created, about to check validaty")
        if form.is_valid():
            print("Form is valid, about to save user")
            user = form.save()
            print(f"User {user.username} created successfully, about to log in")
            username = form.cleaned_data.get('username')
            messages.success(request, f"Account created for {username}!")
            print(f"Redirecting to home page")
            return redirect('home')
        else:
            print("Form is not valid, errors:", form.errors.as_json())
            messages.error(request, "Failed to create account. Please correct your details.")
    else:
        print("GET request received, creating empty form")
        form = CustomUserCreationForm()

    context = { 'register_form': form, 'page': 'register' }
    return render(request, 'blog/register.html', context)

@login_required
def profile(request):
    if request.method == 'POST':
        updateform =  UserUpdateForm(request.POST, instance=request.user)
        profileform = ProfileUpdateForm(request.POST,request.FILES, instance=request.user.profile)
        if updateform.is_valid() and  profileform.is_valid():
            updateform.save()
            profileform.save()
            messages.success(request,'Your profile has been updated successfully!')
            return redirect('profile')
        else:
            messages.error(request,'Failed to update profile. Please correct the errors and try again.')
    else:
        updateform = UserUpdateForm(instance=request.user)
        profileform = ProfileUpdateForm(instance=request.user.profile)
        context = {'u_form': updateform, 'profile_form': profileform}
    return render(request, 'profile.html', context)

def login_view(request):

    if request.user.is_authenticated:
        messages.info(request, 'You are already logged in.')
        return redirect('blog-home')
    
    next_url = request.GET.get('next')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {username}!')
            # Redirect to 'next' if it exists, otherwise default
            if next_url:
                return redirect(next_url)
            return redirect('blog-home')
        else:
            messages.error(request, 'Invalid username or password.')
    

    context = {'page': 'login'}
    return render(request, 'blog/login.html', context)

def logout_view(request):
    # Handle logout logic here
    logout(request)
    messages.success(request,'You have been logged out successfully.')
    return redirect('blog-home')


def home(request):
    print("=== home view ===") 
    posts = Post.objects.all()
    context = {'posts':posts    }
    return render(request, 'home.html',context)
