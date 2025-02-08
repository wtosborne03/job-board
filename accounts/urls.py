from django.urls import path
from .views import login_view, register_view, profile_view, logout_view, onboarding_view, edit_company_info, edit_job_seeker_info
from .views import CustomPasswordResetView, CustomPasswordResetDoneView, CustomPasswordResetConfirmView, CustomPasswordResetCompleteView

urlpatterns = [
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("profile/", profile_view, name="profile"),
    path("profile/edit_company_info/",
         edit_company_info, name="edit_company_info"),
    path("profile/edit_job_seeker_info/",
         edit_job_seeker_info, name="edit_job_seeker_info"),
    path("onboarding/", onboarding_view, name="onboarding"),

    path("logout/", logout_view, name="logout"),
    path("password_reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", CustomPasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("reset/<uidb64>/<token>/", CustomPasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("reset/done/", CustomPasswordResetCompleteView.as_view(),
         name="password_reset_complete"),
]
