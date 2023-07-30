from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index),
    # Biography view (change class-based generic view to a normal view)
    path('biography/', views.BiographyAPI.as_view()),
    path('delete_biography/<int:bio_id>/', views.delete_biography, name='delete_biography'),
    # Project view
    path('projects/', views.ViewAndCreateProjectsAPI.as_view()),
    path('projects/recent_projects/', views.ViewAndCreateCurrProjAPI.as_view()), # moved above potential crosspath url
    path('projects/notes/', views.ViewAndCreateProjNotesAPI.as_view()), # moved above potential crosspath url
    path('projects/view_project/<slug:proj_slug>/', views.UpdateProjectAPI.as_view()), # careful for crosspaths with the url above
    # Contact Me View
    path('contact_me/', views.ViewAndCreateContactMesAPI.as_view()),
    path('contact_me/all_inquries/', views.view_all_contact_mes),
    path('contact_me/<int:contact_id>/', views.UpdateContactMeAPI.as_view()),
    # Feedback View
    path('contact_me/feedback/', views.ViewAndCreateFeedbackAPI.as_view()),
    # Profile Views
    # path('profile/', views.ViewAndCreateSocialsProfileAPI.as_view()),

    # Resume Views

    # NEED TESTING VIEWS
    # path('projects/notes/<int:proj_notes_id>/', views.UpdateProjNotesAPI.as_view()),
    path('resume/', views.FullResumeAPI.as_view()),
    path('resume/projects/', views.ViewAndCreateResumeProjectsAPI.as_view()),
    path('resume/projects/<slug:resume_slug>/', views.UpdateResumeProjectsAPI.as_view()),
    path('resume/awards/', views.ViewAndCreateResumeAwardsAndAchievementsAPI.as_view()),
    path('resume/awards/<int:id>/', views.UpdateResumeAwardsAndAchievementsAPI.as_view()),
    path('profile/', views.view_create_update_profile),
    path('profile/socials/', views.ViewAndCreateSocialsProfileAPI.as_view()),
    path('profile/socials/<int:socials_id>/', views.UpdateSocialsProfileAPI.as_view()),
]