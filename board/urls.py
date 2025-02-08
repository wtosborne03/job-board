from django.urls import path
from .views import HomeView, EmployerHomeView, CreateListingView, JobDetailView, JobEditView, JobDeleteView, search, CompanyDetailView, SkillAutocomplete, BenefitsAutocomplete, inbox_view, send_message_view, UserAutocomplete, MessageDetailView, JobSeekerDetailView, ApplicationCreateView, ApplicationDetailView, MyApplicationsView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('employer_home/', EmployerHomeView.as_view(), name='employer_home'),

    path('search/', search, name='search'),

    path('job/<int:pk>/', JobDetailView.as_view(), name='job_detail'),
    path('job/<int:pk>/edit/', JobEditView.as_view(), name='edit_job'),
    path('job/<int:pk>/delete/', JobDeleteView.as_view(), name='delete_job'),

    path('company/<int:pk>/', CompanyDetailView.as_view(), name='company_detail'),
    path('job_seeker/<int:pk>/', JobSeekerDetailView.as_view(),
         name='job_seeker_detail'),


    path('employer/create_listing/',
         CreateListingView.as_view(), name='create_listing'),

    path('inbox/', inbox_view, name='inbox'),
    path('inbox/send_message/', send_message_view, name='send_message'),
    path('message/<int:pk>/', MessageDetailView.as_view(), name='message_detail'),

    path('job/<int:pk>/apply/', ApplicationCreateView.as_view(), name='apply_job'),
    path('application/<int:pk>/', ApplicationDetailView.as_view(),
         name='application_detail'),

    path('my_applications/', MyApplicationsView.as_view(), name='my_applications'),



    path('autocomplete/skills-autocomplete/',
         SkillAutocomplete.as_view(), name='skills-autocomplete'),
    path('autocomplete/benefits-autocomplete/', BenefitsAutocomplete.as_view(),
         name='benefits-autocomplete'),
    path('autocomplete/user-autocomplete/',
         UserAutocomplete.as_view(), name='user-autocomplete'),


]
