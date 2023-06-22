from django.urls import path, include
from . import views

urlpatterns = [
    # path('', views.index),
    # Biography view (change class-based generic view to a normal view)
    path('biography/', views.BiographyAPI.as_view()),
    path('delete_biography/<int:bio_id>/', views.delete_biography, name='delete_biography'),
    # Project view
    path('projects/', views.ViewAndCreateProjectsAPI.as_view()),
    path('projects/<slug:proj_slug>/', views.UpdateProjectAPI.as_view()),
    # Contact Me View
    path('contact_me/', views.ViewAndCreateContactMesAPI.as_view()),
    path('contact_me/all_inquries/', views.view_all_contact_mes),
    path('contact_me/<int:contact_id>/', views.UpdateContactMeAPI.as_view()),
    # Profile Views
    path('profile/', views.ViewSocialsProfileAPI.as_view()),
    # Resume Views
    path('resume/', views.ViewResumeAPI.as_view()),
]