# We are going to make some serializers for our front-end
from rest_framework import serializers
from .models import *   # importing all models\
from django.http import JsonResponse



class BiographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Biography
        fields = '__all__'


class SocialsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialsProfile
        fields = (
            'id',
            'social_name',
            'info',
            'info_link',
            'info_icon',
            'info_color',
            'profile'
        )


class ProfileSerializer(serializers.ModelSerializer):
    socials = SocialsProfileSerializer(many=True, allow_null=True, required=False)
    biography = BiographySerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Profile
        fields = ('id', 'full_name', 'quick_description', 'socials', 'biography')


class CurrProjSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrProj
        fields = "__all__"


# class ProjNotesRequirement:
#     def __init__(self, base):
#         self.base = base
#
#     def __call__(self, project_id, resume_project_id):
#         if project_id is null and resume_project_id is null:
#             msg = "This Note instance must be associated with a Project ID or Resume Project ID"
#             raise serializers.ValidationError(msg)


class ProjectNotesSerializer(serializers.ModelSerializer):
    # just remember resume project notes and normal project notes are included
    def validate(self,data):
        """
        Check if Project Notes have a Project ID or Resume Project ID (has to be either one) not both
        """

        # we need to use the get method to prevent KeyErrors .get(key, [default_value])
        if data.get('project', None) is None and data.get('resume_project', None) is None:
            msg = "This Note instance must be associated with a Project ID or Resume Project ID"
            raise serializers.ValidationError({'message':msg})
        elif data.get('project', None) is not None and data.get('resume_project', None) is not None:
            msg = "This Note instance must be associated with ONE Project ID or Resume Project ID... not both"
            raise serializers.ValidationError({'message': msg})

    class Meta:
        model = ProjectNotes
        fields = (
            'id',
            'init_notes',
            'final_notes',
            'project_notes',
            'project',
            'resume_project',
        )
        # extra_kwargs = {'client': {'required': False}}    # we can't use this because we need either or
        # validators = [ProjNotesRequirement()]


class ProjectSerializer(serializers.ModelSerializer):
    proj_img_url = serializers.SerializerMethodField('get_proj_img_url')
    proj_notes = ProjectNotesSerializer(many=True, allow_null=True, required=False)
    learnings = serializers.SerializerMethodField('get_learnings')
    tools = serializers.SerializerMethodField('get_tools')

    class Meta:
        model = Project
        fields = (
            'id',
            'proj_name',
            'proj_img',
            'proj_img_url',
            'proj_description',
            'proj_url',
            'proj_notes',
            'proj_date',
            'showcasing',
            'showcasing_url',
            'proj_slug',
            'learnings',
            'tools',
        )

    def get_proj_img_url(self, obj):
        return obj._get_image_url()

    def get_learnings(self, obj):
        return obj.listify_field(obj.proj_learnings)

    def get_tools(self, obj):
        return obj.listify_field(obj.proj_tools)


class ContactMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMe
        fields = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            'feedback_option',
            'user_email',
            'user_fb_desc',
            'user_web_fb_ans',
            'get_feedback_statements',
            'get_feedback_answers',
        )

"""
    null value in column "profile_id" of relation "jdwebport_app_resume" violates not-null constraint
    The issue is that we have a profile field within ResumeSerializer which interferes with POST request because it 
    requires a Profile dictionary and when given ProfileSerializer(profile_query).data it still yields the same error 
    therefore we're going to create another resumeserializer that's postable and keep the current one is a get serializer
"""


class POSTResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class ResumeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(allow_null=True, required=False, read_only=True)
    rel_courses = serializers.SerializerMethodField('get_rel_courses')
    lang = serializers.SerializerMethodField('get_lang')
    fw = serializers.SerializerMethodField('get_fw')
    tools = serializers.SerializerMethodField('get_tools')

    def get_rel_courses(self, resume):
        return resume.listify_field(resume.school_rel_courses)

    def get_lang(self, resume):
        return resume.listify_field(resume.skills_lang)

    def get_fw(self, resume):
        return resume.listify_field(resume.skills_fw)

    def get_tools(self, resume):
        return resume.listify_field(resume.skills_tools)

    class Meta:
        model = Resume
        fields = ('id',
                  'profile',
                  'school_name',
                  'school_loc',
                  'school_gpa',
                  'school_degree',
                  'rel_courses',
                  'lang',
                  'fw',
                  'tools',
        )


class ResumeProjectsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeProjects
        fields = (
            'id',
            'project_name',
            'resume_slug',
            'resume'
        )


class ResumeAwardsAndAchievementsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeAwardsAndAchievements
        fields = (
            'id',
            'award_achievement_name',
            'initial_date',
            'final_date',
            'duration',
            'resume'
        )