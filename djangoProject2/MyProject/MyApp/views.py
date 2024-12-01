from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import get_user_model
from .forms import UserProfileForm, PasswordChangeForm, DeleteAccountForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def delete_account_view(request):
    if request.method == 'POST':
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.cleaned_data['confirm']:
            request.user.delete()
            messages.success(request, "Your account has been deleted.")
            return redirect('home')  # Redirect to the home page or login page after account deletion
    else:
        form = DeleteAccountForm()

    return render(request, 'delete_account.html', {'form': form})

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Redirect back to profile page after saving
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'edit_profile.html', {'form': form})

@login_required
def change_password_view(request):
    if request.method == 'POST':
        # Pass the current user instance to the form
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            # Update session auth hash to keep the user logged in after changing the password
            update_session_auth_hash(request, form.user)
            messages.success(request, "Your password has been successfully changed!")
            return redirect('profile')
    else:
        form = PasswordChangeForm(user=request.user)

    return render(request, 'change_password.html', {'form': form})

@login_required
def profile_view(request):
    profile_form = UserProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    delete_form = DeleteAccountForm()

    if request.method == "POST":
        if "edit_profile" in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "Profile updated successfully.")
                return redirect('profile')

        elif "change_password" in request.POST:
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                messages.success(request, "Password changed successfully.")
                return redirect('profile')

        elif "delete_account" in request.POST:
            delete_form = DeleteAccountForm(request.POST)
            if delete_form.is_valid() and delete_form.cleaned_data['confirm']:
                request.user.delete()
                messages.success(request, "Your account has been deleted.")
                return redirect('home')

    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'delete_form': delete_form,
    }
    return render(request, 'profile.html', context)

User = get_user_model()

def user_list_view(request):
    users = User.objects.all()
    return render(request, "user_list.html", {"users": users})

def logout_view(request):
    """Logs out the user and redirects to the login page."""
    logout(request)
    return redirect("login")  # Ensure "login" is the name of your login URL pattern

@login_required
def dashboard_view(request):
    # Fetch user-specific data here if needed
    return render(request, "dashboard.html")

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, username=email, password=password)
        if user:
            login(request, user)
            return redirect("/dashboard/")
        else:
            messages.error(request, "Invalid email or password")
    return render(request, "login.html")

def register_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        role = request.POST.get("role")  # Get the selected role from the form

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
        elif User.objects.filter(username=email).exists():
            messages.error(request, "Email is already registered")
        else:
            user = User.objects.create_user(username=email, email=email, password=password, first_name=username)
            user.role = role  # Save the role
            user.save()
            messages.success(request, "Registration successful!")
            return redirect("/login/")
    return render(request, "register.html")
