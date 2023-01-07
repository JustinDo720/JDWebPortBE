from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view


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
        bio_query = Biography.objects.latest('id')  # we want to get the latest id in case we del id=1 row
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