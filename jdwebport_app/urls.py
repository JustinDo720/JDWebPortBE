from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index),
    # Biography view (change class-based generic view to a normal view)
    path('biography/', views.BiographyAPI.as_view()),
    path('biography/section/', views.BiographySectionAPI.as_view()),
    path('biography/section/<slug:section_slug>/', views.UpdateBiographySectionAPI.as_view()),
    path('biography/section-imgs/', views.BiographySectionImgAPI.as_view()),
    path('biography/section-imgs/<slug:section_img_slug>/', views.UpdateBiographySectionImgAPI.as_view()),
    path('biography/delete_biography/<int:bio_id>/', views.delete_biography, name='delete_biography'),

    # Project view
    path('projects/', views.ViewAndCreateProjectsAPI.as_view()),
    path('projects/recent_projects/', views.ViewAndCreateCurrProjAPI.as_view()), # moved above potential crosspath url
    path('projects/recent_projects/<slug:curr_proj_slug>/', views.UpdateCurrProjAPI.as_view()),
    path('projects/notes/', views.ViewAndCreateProjNotesAPI.as_view()), # moved above potential crosspath url
    path('projects/view_project/<slug:proj_slug>/', views.UpdateProjectAPI.as_view()), # careful for crosspaths with the url above
    # Contact Me View
    path('contact_me/', views.ViewAndCreateContactMesAPI.as_view()),
    path('contact_me/all_inquries/', views.view_all_contact_mes),
    path('contact_me/<int:contact_id>/', views.UpdateContactMeAPI.as_view()),
    # Feedback View
    path('contact_me/feedback/', views.ViewAndCreateFeedbackAPI.as_view()),
    path('contact_me/feedback_question/', views.ViewFeedbackQuestionAPI.as_view()),
    # Profile Views
    path('profile/', views.view_create_update_profile),
    path('profile/socials/', views.ViewAndCreateSocialsProfileAPI.as_view()),
    path('profile/socials/<int:socials_id>/', views.UpdateSocialsProfileAPI.as_view()),

    # Resume Views
    path('resume/', views.FullResumeAPI.as_view()),
    path('resume/projects/', views.ViewAndCreateResumeProjectsAPI.as_view()),
    path('resume/projects/<slug:resume_slug>/', views.UpdateResumeProjectsAPI.as_view()),
    path('resume/awards/', views.ViewAndCreateResumeAwardsAndAchievementsAPI.as_view()),
    path('resume/awards/<int:id>/', views.UpdateResumeAwardsAndAchievementsAPI.as_view()),

    # NEED TESTING VIEWS
    path('resume/project_details/', views.ViewAndCreateResumeProjectDetailsAPI.as_view()),  # Create and view all Resume Project Details
    path('resume/project_details/<int:resume_project_id>/', views.update_resume_project_details),    # update, delete and view specific Resume Project Details
    path('projects/images/', views.ViewAndCreateProjImgAPI.as_view()),
    path('projects/images/<slug:project_image_slug>/', views.UpdateProjImgAPI.as_view())

]