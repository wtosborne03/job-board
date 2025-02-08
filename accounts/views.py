from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm, EmployerInformationForm, JobSeekerInformationForm
from .forms import EmployerOnboardingForm, JobSeekerOnboardingForm
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .forms import CustomPasswordResetForm
from .models import UserProfile


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("profile")
    else:
        form = CustomAuthenticationForm()
    return render(request, "accounts/login.html", {"form": form})


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                form.instance.username = form.instance.email
                user = form.save()
                user_type = form.cleaned_data['user_type']
                UserProfile.objects.create(
                    user=user, user_type=user_type)  # Add user_type here
                messages.info(
                    request, "Thanks for registering. You are now logged in.")
                new_user = authenticate(username=form.cleaned_data['email'],
                                        password=form.cleaned_data['password1'])
                login(request, new_user)
                return redirect("onboarding")
            except Exception as e:
                messages.error(request, e)
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile_view(request):
    return render(request, "accounts/profile/profile.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Logged Out")
    return redirect("login")


@login_required
def onboarding_view(request):
    user = request.user

    if hasattr(user, 'userprofile'):
        profile = user.userprofile
    else:
        profile = None

    if profile.completed_onboarding:
        return redirect("home")  # If already onboarded, go to dashboard

    if profile.user_type == "employer":
        form = EmployerOnboardingForm(
            request.POST or None, request.FILES or None)
    else:
        form = JobSeekerOnboardingForm(
            request.POST or None, request.FILES or None)

    if request.method == "POST" and form.is_valid():
        onboarding = form.save(commit=False)
        onboarding.user = request.user
        onboarding.save()
        profile.completed_onboarding = True
        profile.save()
        return redirect("home")  # Redirect to main app

    return render(request, "accounts/onboarding.html", {"form": form})


@login_required
def edit_company_info(request):
    if request.user.userprofile.user_type != 'employer':
        return redirect('profile')
    if request.method == 'POST':
        form = EmployerInformationForm(
            request.POST, request.FILES, instance=request.user.employerprofile)  # Add request.FILES
        if form.is_valid():
            form.save()
            messages.info(request, "Profile Updated")
            return redirect('edit_company_info')
    else:
        form = EmployerInformationForm(instance=request.user.employerprofile)
    return render(request, 'accounts/profile/edit_company_info.html', {'form': form})


@login_required
def edit_job_seeker_info(request):
    if request.user.userprofile.user_type != 'job_seeker':
        return redirect('profile')
    if request.method == 'POST':
        form = JobSeekerInformationForm(
            request.POST, request.FILES, instance=request.user.jobseekerprofile)
        if form.is_valid():
            form.save()
            messages.info(request, "Profile Updated")
            return redirect('edit_job_seeker_info')
    else:
        form = JobSeekerInformationForm(instance=request.user.jobseekerprofile)
    return render(request, 'accounts/profile/edit_job_seeker_info.html', {'form': form})


class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset/password_reset.html'
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'accounts/password_reset/password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'accounts/password_reset/password_reset_confirm.html'


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'accounts/password_reset/password_reset_complete.html'
