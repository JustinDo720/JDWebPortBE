from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .pagination import ProjectResultsSetPagination, ContactMeResultsSetPagination
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
# def index(request):
#     return render(request, 'index.html')

# View sets for the restframework page
class BiographyViewSet(viewsets.ModelViewSet):
    queryset = Biography.objects.all()
    serializer_class = BiographySerializer


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ContactMeViewSet(viewsets.ModelViewSet):
    queryset = ContactMe.objects.all()
    serializer_class = ContactMeSerializer


# Api endpoints to perform actions

class BiographyAPI(APIView):
    """
    View to look at our biography information as well as adding and editing one biography instance

        * Requires an Admin Authentication
        * Admin users can access this view
        * GET, POST, PUT are the handler methods that we're going to be using
    """

    def get(self, request):
        """
        returns our bio info
        """

        # sometimes we might have not one in our db so we need to take that into account
        try:
            bio_query = Biography.objects.latest('id')  # we want to get the latest id in case we del id=1 row
        except Exception:
            bio_query = None
        serializer = BiographySerializer(bio_query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        adds a new biography instance
        """
        serializer = BiographySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        """
        edits our current biography instance
        """
        bio_query = Biography.objects.latest('id')
        serializer = BiographySerializer(bio_query, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
def delete_biography(request, bio_id):
    """
    deletes a biography instance
    """
    bio_query = Biography.objects.get(id=bio_id)
    bio_query.delete()
    return Response({'message': 'Your biography has been deleted'}, status=status.HTTP_200_OK)


class ViewAndCreateProjectsAPI(generics.ListCreateAPIView):
    """
    View all the Projects in our database
        * this is allowed for everyone to see

    Create Projects to our database
        * only admin users can do that
    """
    queryset = Project.objects.all()   # we dont need to overwrite get_queryset() bc there are no filters
    serializer_class = ProjectSerializer
    pagination_class = ProjectResultsSetPagination

    # we do, however, need to overwrite the create function
    def create(self, request, *args, **kwargs):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid(): # we don't need proj notes to create a proj
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProjectAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Update a Project; given a project slug

        * Generic View to Retrieve(GET), Update(PUT), Destroy(DELETE)
    """

    serializer_class = ProjectSerializer

    # we are going to need to overwrite get_queryset bc generics.RetrieveUpdateDestroyAPIView needs a slug
    def get_queryset(self, *args, **kwargs):
        proj_slug = self.kwargs.get('proj_slug')
        proj_obj = Project.objects.get(proj_slug=proj_slug)
        return proj_obj # return some query based off our proj slug

    # creating the retrieve function
    def retrieve(self, request, *args, **kwargs):
        proj_obj = self.get_queryset()
        serializer = ProjectSerializer(proj_obj)
        return Response(serializer.data)

    # creating the update function
    def update(self, request, *args, **kwargs):
        proj_obj = self.get_queryset()
        serializer = ProjectSerializer(proj_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # creating the destroy function
    def destroy(self, request, *args, **kwargs):
        proj_obj = self.get_queryset()
        proj_obj.delete()
        return Response({'message': 'Your project has been deleted'}, status=status.HTTP_200_OK)


@api_view(['GET'])
def view_all_contact_mes(request):
    """
    View all the Contact Mes in our database
        * This gathers every contact me (completed or incomplete)
    """
    contact_mes = ContactMe.objects.all()
    serializer = ContactMeSerializer(contact_mes, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


class ViewAndCreateContactMesAPI(generics.ListCreateAPIView):
    """
    View Contact Mes that are incomplete in our database
        * this is allowed for everyone to see

    Create Contact Mes to our database
        * only admin users can do that
    """
    queryset = ContactMe.objects.filter(inquiry_accomplished=False) # want active inquiries
    serializer_class = ContactMeSerializer
    pagination_class = ContactMeResultsSetPagination
    permission_classes = [permissions.AllowAny]


class UpdateContactMeAPI(generics.RetrieveUpdateDestroyAPIView):
    """
    Update a ContactMe; given a ContactMe ID

        * Generic View to Retrieve(GET), Update(PUT), Destroy(DELETE)
    """

    serializer_class = ContactMeSerializer

    # we are going to need to overwrite get_queryset bc generics.RetrieveUpdateDestroyAPIView needs a slug
    def get_queryset(self, *args, **kwargs):
        contact_id = self.kwargs.get('contact_id')
        contact_obj = ContactMe.objects.get(id=contact_id)
        return contact_obj # return some query based off our contact id

    # creating the retrieve function
    def retrieve(self, request, *args, **kwargs):
        contact_obj = self.get_queryset()
        serializer = ContactMeSerializer(contact_obj)
        return Response(serializer.data)

    # creating the update function
    def update(self, request, *args, **kwargs):
        contact_obj = self.get_queryset()
        serializer = ContactMeSerializer(contact_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # creating the destroy function
    def destroy(self, request, *args, **kwargs):
        contact_obj = self.get_queryset()
        contact_obj.delete()
        return Response({'message': 'Your inquiry has been deleted'}, status=status.HTTP_200_OK)


class ViewSocialsProfileAPI(APIView):
    def get(self, request):
        """
        returns our bio info
        """

        # sometimes we might have not one in our db so we need to take that into account
        try:
            profile_query = Profile.objects.latest('id')  # we want to get the latest id in case we del id=1 row
        except Exception:
            profile_query = None
        serializer = ProfileSerializer(profile_query)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewResumeAPI(APIView):

    def get(self, request):
        try:
            resume_query = Resume.objects.latest('id')  # we want to get the latest id in case we del id=1 row
        except Exception:
            resume_query = None
        serializer = ResumeSerializer(resume_query)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ViewAndCreateFeedbackAPI(generics.ListCreateAPIView):
        queryset = Feedback.objects.all()
        serializer_class = FeedbackSerializer
        pagination_class = ContactMeResultsSetPagination # reusing that 10 ContactMe Results for Feedback API
        permission_classes = [permissions.AllowAny]


class ViewAndCreateCurrProjAPI(generics.ListCreateAPIView):
    queryset = CurrProj.objects.all()[:3]
    serializer_class = CurrProjSerializer
    permission_classes = [permissions.AllowAny]