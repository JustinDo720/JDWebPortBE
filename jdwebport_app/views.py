from django.shortcuts import render
from rest_framework import viewsets, status
from .serializers import *
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .pagination import ProjectResultsSetPagination, ContactMeResultsSetPagination, ResumeProjectPagination, ResumeAwardsAndAchievementsPagination
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
import datetime


# Create your views here.
# def index(request):
#     return render(request, 'index.html')


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
            bio_query = Biography.objects.all()
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
        serializer = BiographySerializer(bio_query, data=request.data, partial=True)
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


class BiographySectionAPI(generics.ListCreateAPIView):
    queryset = BiographySection.objects.all()
    serializer_class = BiographySectionSerializer

    # ONly necessary for post requests for all users
    # permission_classes = [permissions.AllowAny] we don't need this because we have our default permission.
    def create(self, request, *args, **kwargs):
        if Biography.objects.count() >= 1:
            request.data['biography'] = Biography.objects.all().latest('id').id
        else:
            return Response({'msg': "Please create a Biography instance first before creating sections"}, status=status.HTTP_200_OK)
        serializer = BiographySectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBiographySectionAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'section_slug'

    def get_queryset(self, *args, **kwargs):
        try:
            bio_sec = BiographySection.objects.get(section_slug=self.kwargs.get('section_slug'))
            return bio_sec
        except BiographySection.DoesNotExist:
            raise Http404   # raising http404 if it doesnt exist is better than passing a queryset...

    def retrieve(self, request, *args, **kwargs):
        bio_sec = self.get_queryset()
        serializer = BiographySectionSerializer(bio_sec)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        bio_sec = self.get_queryset()
        serializer = BiographySectionSerializer(bio_sec, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        bio_sec = self.get_queryset()
        bio_sec.delete()
        return Response({'message': 'Your Biography Section has been deleted'}, status=status.HTTP_200_OK)


class BiographySectionImgAPI(APIView):
    def get(self, request):
        biography_img = BiographySectionImage.objects.all()
        serializer = BiographySectionImgSerializer(biography_img, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = BiographySectionImgSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateBiographySectionImgAPI(generics.RetrieveUpdateDestroyAPIView):
    lookup_field = 'section_img_slug'
    serializer_class = BiographySectionImgSerializer

    def get_queryset(self, *args, **kwargs):
        section_img_slug = self.kwargs.get('section_img_slug')
        bio_sec_img = BiographySectionImage.objects.get(section_img_slug=section_img_slug)
        return bio_sec_img # return some query based off our proj slug

    def retrieve(self, request, *args, **kwargs):
        bio_sec_img = self.get_queryset()
        serializer = BiographySectionImgSerializer(bio_sec_img)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        bio_sec_img = self.get_queryset()
        serializer = BiographySectionImgSerializer(bio_sec_img, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        bio_sec_img = self.get_queryset()
        bio_sec_img.delete()
        return Response({'message': 'Your Biography Image has been deleted'}, status=status.HTTP_200_OK)


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
        serializer = ProjectSerializer(proj_obj, context={'request':request}) # context may not be necessary for production
        return Response(serializer.data)

    # creating the update function
    def update(self, request, *args, **kwargs):
        proj_obj = self.get_queryset()
        if request.data.get('proj_name', None):
            # get another slug because the slug changes with the title
            new_slug = proj_obj._get_unique_slug()
            request.data['proj_slug'] = new_slug
        serializer = ProjectSerializer(proj_obj, data=request.data, partial=True, context={'request':request}) # context may not be necessary for production
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
    parser_classes = (MultiPartParser,)
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

    def create(self, request, *args, **kwargs):
        serializer = ContactMeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


@api_view(['GET','POST','PUT'])
def view_create_update_profile(request):
    """
        Creates a profile instance
        View the Profile Instance
        Update the Profile Instance

        We might not need to delete this instance because we NEED one profile instance for this website to work properly
    """
    if request.method == 'POST' and Profile.objects.count() < 1:
        # like I said there could only be one Profile instance so we will post if the count is less than 1
        serializers = ProfileSerializer(data=request.data, context={'request': request})
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST' and Profile.objects.count() >= 1:
        return Response({'msg': "We only accept one Profile Instance"}, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        permission_classes = [permissions.AllowAny]
        profile_query = Profile.objects.latest('id')
        profile_serializer = ProfileSerializer(profile_query, context={'request': request})
        return Response(profile_serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        profile_query = Profile.objects.latest('id')
        profile_serializer = ProfileSerializer(profile_query, data=request.data, partial=True, context={'request': request})  # no full field validation check
        if profile_serializer.is_valid():
            profile_serializer.save()
            return Response(profile_serializer.data, status=status.HTTP_200_OK)
        return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateSocialsProfileAPI(APIView):
    """
        View, Update, or Delete a specific instance of SocialsProfile
    """
    def get(self, request, socials_id):
        specific_social = SocialsProfile.objects.get(id=socials_id)
        serializer = SocialsProfileSerializer(specific_social)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, socials_id):
        specific_social = SocialsProfile.objects.get(id=socials_id)
        serializer = SocialsProfileSerializer(specific_social, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, socials_id):
        SocialsProfile.objects.get(id=socials_id).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewAndCreateSocialsProfileAPI(APIView):
    def get(self, request):
        """
        returns Socials Profile (all of our socials within the Profile)
        create more social instances for our profile
        """

        socials_query = SocialsProfile.objects.all()
        if socials_query.count() == 0:
            socials_query = None

        """
        Note: make sure to set many on our serializer to handle multiple instances or else you'll get the error below
        
        The serializer field might be named incorrectly and not match any attribute or key on the `QuerySet` instance.
            Original exception text was: 'QuerySet' object has no attribute 'social_name'.
        """
        serializer = SocialsProfileSerializer(socials_query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        request.data['profile'] = Profile.objects.latest('id').id
        socials_serializer = SocialsProfileSerializer(data=request.data)
        if socials_serializer.is_valid():
            socials_serializer.save()
            return Response(socials_serializer.data, status=status.HTTP_201_CREATED)
        return Response(socials_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FullResumeAPI(APIView):
    """
        Return the lastest Resume (could only be one real resume)
        Post Information for that Resume
        Update Information for that Resume
        Remove That resume
    """

    def get(self, request):
        try:
            resume_query = Resume.objects.latest('id')  # we want to get the latest id in case we del id=1 row
        except Exception:
            resume_query = None
        serializer = ResumeSerializer(resume_query)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if Resume.objects.count() < 1:
            # here's the issue, we can't post with a nested serializer therefore we created a sep serializer for POST req
            request.data['profile'] = Profile.objects.latest('id').id
            serializer = POSTResumeSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"msg":"There could only be one Resume Instance"}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        # we dont need a resume id or slug because there could only be ONE resume
        resume_query = Resume.objects.latest('id')
        resume_serializer = ResumeSerializer(resume_query, data=request.data, partial=True) # similar to POST request
        if resume_serializer.is_valid():
            resume_serializer.save()
            return Response(resume_serializer.data, status=status.HTTP_200_OK)
        return Response(resume_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        resume_query = Resume.objects.latest('id')
        resume_query.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UpdateResumeProjectsAPI(generics.RetrieveUpdateDestroyAPIView): # RetrieveUpdateDestroyAPIView needs a pk
    queryset = ResumeProjects.objects.all()
    serializer_class = ResumeProjectsSerializer
    pagination_class = ResumeProjectPagination
    lookup_field = 'resume_slug'  # our pk is slug so we set it with lookup_field

    def update(self, request, *args, **kwargs):
        # since we have one resume we could include that to streamline our post process
        request.data['resume'] = Resume.objects.latest('id').id
        resume_project = ResumeProjects.objects.get(resume_slug=self.kwargs["resume_slug"])
        if request.data.get('project_name', None):
            # get another slug because the slug changes with the title
            new_slug = resume_project._get_unique_slug()
            request.data['resume_slug'] = new_slug
        resume_project_serializer = ResumeProjectsSerializer(resume_project, data=request.data, partial=True)
        if resume_project_serializer.is_valid():
            resume_project_serializer.save()
            return Response(resume_project_serializer.data, status=status.HTTP_200_OK)
        return Response(resume_project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# we need to worry about getting all the resume projects and posting them
class ViewAndCreateResumeProjectsAPI(generics.ListCreateAPIView):
    queryset = ResumeProjects.objects.all()
    serializer_class = ResumeProjectsSerializer
    pagination_class = ResumeProjectPagination

    def create(self, request, *args,):
        request.data['resume'] = Resume.objects.latest('id').id
        resume_project_serializer = ResumeProjectsSerializer(data=request.data)
        if resume_project_serializer.is_valid():
            resume_project_serializer.save()
            return Response(resume_project_serializer.data, status=status.HTTP_200_OK)
        return Response(resume_project_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateResumeAwardsAndAchievementsAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResumeAwardsAndAchievements.objects.all()
    serializer_class = ResumeAwardsAndAchievementsSerializer
    pagination_class = ResumeAwardsAndAchievementsPagination
    lookup_field = 'id'

    def update(self, request, *args, **kwargs):
        request.data['resume'] = Resume.objects.latest('id').id
        resume_awards = ResumeAwardsAndAchievements.objects.get(id=self.kwargs["id"])
        resume_awards_serializer = ResumeAwardsAndAchievementsSerializer(resume_awards, data=request.data, partial=True)
        if resume_awards_serializer.is_valid():
            resume_awards_serializer.save()
            return Response(resume_awards_serializer.data, status=status.HTTP_200_OK)
        return Response(resume_awards_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewAndCreateResumeAwardsAndAchievementsAPI(generics.ListCreateAPIView):
    queryset = ResumeAwardsAndAchievements.objects.all()
    serializer_class = ResumeAwardsAndAchievementsSerializer
    pagination_class = ResumeAwardsAndAchievementsPagination

    def create(self, request, *args,):
        request.data['resume'] = Resume.objects.latest('id').id

        # we need to work on the duration here
        initial_date = request.data['initial_date'].split('-')
        initial_datetime = datetime.date(int(initial_date[0]), int(initial_date[1]), int(initial_date[2]))
        final_date = request.data['final_date'].split('-')
        final_datetime = datetime.date(int(final_date[0]), int(final_date[1]), int(final_date[2]))

        time_duration = final_datetime - initial_datetime # a time delta of days (duration field is only in days
        request.data['duration'] = time_duration

        resume_awards_serializer = ResumeAwardsAndAchievementsSerializer(data=request.data)
        if resume_awards_serializer.is_valid():
            resume_awards_serializer.save()
            return Response(resume_awards_serializer.data, status=status.HTTP_200_OK)
        return Response(resume_awards_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ViewAndCreateResumeProjectDetailsAPI(APIView):
    # Focus on creating and ALL viewing the project details
    def get(self, request):
        query = ResumeProjectDetails.objects.all()
        serializer = ResumeProjectDetailsSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ResumeProjectDetailsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def update_resume_project_details(request,resume_project_id):
    # viewing specific project detail
    query = ResumeProjectDetails.objects.get(id=resume_project_id)
    if request.method == "GET":
        serializer = ResumeProjectDetailsSerializer(query)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == "PUT":
        serializer = ResumeProjectDetailsSerializer(query, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        query.delete()
        return Response({'msg': f"Removed Details for: {query.resume_project.project_name}"}) # flag worthy


class ViewFeedbackQuestionAPI(APIView):

    def get(self, request, *args, **kwargs):
        try:
            latest_fb = Feedback.objects.latest('id')
            latest_fb_question = FeedbackQuestionSerializer(latest_fb)
            return Response(latest_fb_question.data, status=status.HTTP_200_OK)
        except Feedback.DoesNotExist:
            default_data = {
                "user_email": "random@default.com",
                "user_fb_desc": "Default Description for question queries"
            }
            new_fb_obj = Feedback.objects.create(user_email=default_data['user_email'], user_fb_desc=default_data['user_fb_desc'])
            new_fb_obj.save()
            latest_fb_question = FeedbackQuestionSerializer(new_fb_obj)
            return Response(latest_fb_question.data, status=status.HTTP_200_OK)


class ViewAndCreateFeedbackAPI(generics.ListCreateAPIView):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    pagination_class = ContactMeResultsSetPagination # reusing that 10 ContactMe Results for Feedback API
    permission_classes = [permissions.AllowAny]


class ViewAndCreateCurrProjAPI(generics.ListCreateAPIView):
    queryset = CurrProj.objects.all()[:3]
    serializer_class = CurrProjSerializer
    # permission_classes = [permissions.AllowAny]

    def get_permissions(self):  # method works must apply to others
        method = self.request.method
        if method == 'POST':
           return [permissions.IsAuthenticated()]
        else:
           return [permissions.AllowAny()]


class UpdateCurrProjAPI(APIView):
    def put(self, request, *args, **kwargs):
        curr_proj_slug = self.kwargs.get('curr_proj_slug')
        curr_proj = CurrProj.objects.get(curr_proj_slug=curr_proj_slug)
        if request.data.get('focus_title', None):
            # get another slug because the slug changes with the title
            new_slug = curr_proj._get_unique_slug()
            request.data['curr_proj_slug'] = new_slug
        serializers = CurrProjSerializer(curr_proj, data=request.data, partial=True)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        curr_proj_slug = request.data['curr_proj_slug']
        curr_proj = CurrProj.objects.get(curr_proj_slug=curr_proj_slug)
        curr_proj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ViewAndCreateProjNotesAPI(APIView):
    # we just need an api that supports GET and POST. we dont want to view specific notes because Project Serializer has notes

    def get(self, request):
        proj_notes_query = ProjectNotes.objects.all()
        serializer = ProjectNotesSerializer(proj_notes_query, many=True)    # Dont forget many=True
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectNotesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProjNotesAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = ProjectNotes.objects.all()
    serializer_class = ProjectNotesSerializer
    lookup_field = 'proj_notes_id'


class ViewAndCreateProjImgAPI(APIView):

    def get(self, request):
        proj_img_query = ProjectImage.objects.all()
        # context may not be necessary for production
        serializer = ProjectImgSerializer(proj_img_query, many=True, context={"request": request})  # Dont forget many=True
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = ProjectImgSerializer(data=request.data, context={"request": request}) # context may not be necessary for production
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateProjImgAPI(generics.RetrieveUpdateDestroyAPIView):

    def _get_project_image(self, request, *args, **kwargs):
        slug = self.kwargs.get('project_image_slug')
        proj_img_obj = ProjectImage.objects.get(slug=slug)
        return proj_img_obj

    def retrieve(self, request, *args, **kwargs):
        proj_img_obj = self._get_project_image(request, *args, **kwargs)
        serializer = ProjectImgSerializer(proj_img_obj, context={"request": request}) # context may not be necessary for production
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        proj_img_obj = self._get_project_image(request, *args, **kwargs)
        serializer = ProjectImgSerializer(proj_img_obj, data=request.data, partial=True, context={"request": request}) # context may not be necessary for production
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

    def destroy(self, request, *args, **kwargs):
        proj_img_obj = self._get_project_image(request, *args, **kwargs)
        proj_img_obj.delete()
        return Response({'msg': 'Removed Image'})



