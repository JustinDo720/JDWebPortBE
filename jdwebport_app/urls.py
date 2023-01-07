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
]