from rest_framework import viewsets, status
from .serializers import *
from .models import *
from rest_framework.response import Response


# View sets for the restframework page
"""
    Ideally we might want a ViewSet for every model we have
        Profile [x] 
            Completed w/ Hyperlink? [x]
        SocialsProfile [x] 
            Completed w/ Hyperlink? [x]
        Biography [x]   
            Completed w/ Hyperlink? [x]
        BiographySection [x] 
            Completed w/ Hyperlink? [x]
        BiographySectionImage [x] 
            Completed w/ Hyperlink? [x]
        CurrProj [x] 
            Completed w/ Hyperlink? [ ]
        Project [x] 
            Completed w/ Hyperlink? [ ]
        ContactMe [x] 
            Completed w/ Hyperlink? [x]
        Feedback [x] 
            Completed w/ Hyperlink? [x]
        Resume [x] 
            Completed w/ Hyperlink? [ ]
        ResumeProjects [x] 
            Completed w/ Hyperlink? [ ]
        ResumeProjectDetails [x] 
            Completed w/ Hyperlink? [ ]
        ResumeAwardsAndAchievements [x] 
            Completed w/ Hyperlink? [ ]
        ProjectNotes [x] 
            Completed w/ Hyperlink? [ ]
        ProjectImage [x]
            Completed w/ Hyperlink? [ ]
"""

# Profile Viewset
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


class SocialsProfileViewSet(viewsets.ModelViewSet):
    queryset = SocialsProfile.objects.all()
    serializer_class = SocialsProfileSerializer

# Biography Viewset
class BiographyViewSet(viewsets.ModelViewSet):
    queryset = Biography.objects.all()
    serializer_class = BiographySerializer
    if Biography.objects.count() != 0:
        http_method_names = ['get', 'put', 'delete', 'head']


class BiographySectionViewSet(viewsets.ModelViewSet):
    queryset = BiographySection.objects.all()
    serializer_class = BiographySectionSerializer


class BiographySectionImageViewSet(viewsets.ModelViewSet):
    queryset = BiographySectionImage.objects.all()
    serializer_class = BiographySectionImgSerializer


# Project Viewset
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class CurrProjViewSet(viewsets.ModelViewSet):
    queryset = CurrProj.objects.all()
    serializer_class = CurrProjSerializer


class ProjectNotesViewSet(viewsets.ModelViewSet):
    queryset = ProjectNotes.objects.all()
    serializer_class = ProjectNotesSerializer


class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImgSerializer


# Resume Viewset
class ResumeViewSet(viewsets.ModelViewSet):
    queryset = Resume.objects.all()
    serializer_class = ResumeSerializer


class ResumeProjectsViewSet(viewsets.ModelViewSet):
    queryset = ResumeProjects.objects.all()
    serializer_class = ResumeProjectsSerializer


class ResumeProjectDetailsViewSet(viewsets.ModelViewSet):
    queryset = ResumeProjectDetails.objects.all()
    serializer_class = ResumeProjectDetailsSerializer


class ResumeAwardsAndAchievementsViewSet(viewsets.ModelViewSet):
    queryset = ResumeAwardsAndAchievements.objects.all()
    serializer_class = ResumeAwardsAndAchievementsSerializer


# Feedback Viewset
class ContactMeViewSet(viewsets.ModelViewSet):
    queryset = ContactMe.objects.all()
    serializer_class = ContactMeSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer




