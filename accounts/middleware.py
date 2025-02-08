from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse


class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user_profile = getattr(request.user, 'userprofile', None)
            if user_profile and not user_profile.completed_onboarding:
                if request.path != reverse('onboarding') and request.path != reverse("logout"):
                    if 'text/html' in request.META.get('HTTP_ACCEPT', ''):
                        messages.info(
                            request, "Please complete your onboarding.")
                        return redirect('onboarding')
        response = self.get_response(request)
        return response
