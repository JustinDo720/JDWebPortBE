from rest_framework import viewsets, status
from .serializers import *
from .models import *
from rest_framework.response import Response


# View sets for the restframework page
class BiographyViewSet(viewsets.ModelViewSet):
    queryset = Biography.objects.all()
    serializer_class = BiographySerializer
    # if Biography.objects.count() != 0:
    #     http_method_names = ['get', 'put', 'delete', 'head']
    #
    # def post(self, request, *args, **kwargs):
    #     if Biography.objects.count() == 0:
    #         serializer = BiographySerializer(data=request.data)
    #         if serializer.is_valid():
    #             serializer.save()
    #             return Response(serializer.data, status=status.HTTP_200_OK)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         return Response({'Message': 'Biography already exists. Please update or delete it.'})
    #
    # def put(self, request, format=None):
    #     biography = Biography.objects.latest('id')
    #     serializer = BiographySerializer(biography, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def delete(self, request, format=None):
    #     biography = Biography.objects.latest('id')
    #     biography.delete()
    #     return Response({'Message': "Your Biography was removed"})


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContactMeViewSet(viewsets.ModelViewSet):
    queryset = ContactMe.objects.all()
    serializer_class = ContactMeSerializer

"""
    Ideally we might want a ViewSet for every model we have
    Profile 
    SocialsProfile
    Biography [x]
    BiographySection
    BiographySectionImage
    CurrProj
    Project [x]
    ContactMe [x]
    Feedback
    Resume
    ResumeProjects
    ResumeProjectDetails
    ResumeAwardsAndAchievements
    ProjectNotes
    ProjectImage
"""


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    http_method_names = ['get', 'post', 'put', 'delete']


class SocialsProfileViewSet(viewsets.ModelViewSet):
    queryset = SocialsProfile.objects.all()
    serializer_class = SocialsProfileSerializer


class BiographySectionViewSet(viewsets.ModelViewSet):
    queryset = BiographySection.objects.all()
    serializer_class = BiographySectionSerializer


class BiographySectionImageViewSet(viewsets.ModelViewSet):
    queryset = BiographySectionImage.objects.all()
    serializer_class = BiographySectionImgSerializer


class CurrProjViewSet(viewsets.ModelViewSet):
    queryset = CurrProj.objects.all()
    serializer_class = CurrProjSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


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


class ProjectNotesViewSet(viewsets.ModelViewSet):
    queryset = ProjectNotes.objects.all()
    serializer_class = ProjectNotesSerializer


class ProjectImageViewSet(viewsets.ModelViewSet):
    queryset = ProjectImage.objects.all()
    serializer_class = ProjectImgSerializer


