# We are going to make some serializers for our front-end
from rest_framework import serializers
from .models import *   # importing all models\
from django.http import JsonResponse


class BiographySectionImgSerializer(serializers.ModelSerializer):
    # biography_section_slug = serializers.SerializerMethodField('get_biography_section_slug')
    #
    # def get_biography_section_slug(self):
    #

    class Meta:
        model = BiographySectionImage
        fields = (
            'id',
            'biography_section',
            'section_img',
            'section_img_slug',
            # 'biography_section_slug',
        )


class BiographySectionSerializer(serializers.ModelSerializer):
    bio_imgs = BiographySectionImgSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = BiographySection
        fields = (
            'id',
            'section_name',
            'section_info',
            'biography',
            'section_slug',
            'bio_imgs',
        )


class BiographySerializer(serializers.ModelSerializer):
    short_description = serializers.SerializerMethodField('get_short_description')
    bio_section = BiographySectionSerializer(many=True, allow_null=True, required=False)

    def get_short_description(self, bio_obj):
        return bio_obj.get_short_bio_description()

    class Meta:
        model = Biography
        fields = (
            'id',
            'bio_description',
            'bio_section',
            'bio_entry_date',
            'quote',
            'author',
            'profile',
            'short_description',
        )


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
    # we're going to start validating the fields that require comma separated values
    def validate(self, data):
        if data.get('quick_description', None) is not None and ',' not in data.get('quick_description', None)\
                and data.get('quick_description', None).rstrip().split(',')[-1] != "":
            # the data exists, theres not a , in the data, and it doesnt ends with a comma
            msg = "Please use comma separated values to indicate the amount of items you'd like to use in a string format."
            raise serializers.ValidationError({'message':msg})
        return data

    socials = SocialsProfileSerializer(many=True, allow_null=True, required=False)
    biography = BiographySerializer(many=True, allow_null=True, required=False)
    quick_desc = serializers.SerializerMethodField('get_quick_desc')

    def get_quick_desc(self, profile_obj):
        listified_quick_desc = profile_obj.quick_description.replace(", ", ",").split(',')
        return listified_quick_desc[:len(listified_quick_desc) -1] if listified_quick_desc[-1] == "" else listified_quick_desc

    class Meta:
        model = Profile
        fields = ('id', 'full_name', 'quick_description', 'quick_desc', 'socials', 'biography')


class CurrProjSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrProj
        fields = (
            "focus_title",
            "focus_date",
            "focus_info",
            "curr_proj_slug",
        )


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
        return data

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

    def validate(self, data):
        if data.get('proj_learnings', None) is not None and ', ' not in data.get('proj_learnings', None):
            msg = "Please use comma separated values to indicate the amount of items you'd like to use in a string format"
            raise serializers.ValidationError({'message':msg})
        elif data.get('proj_tools', None) is not None and ', ' not in data.get('proj_tools', None):
            msg = "Please use comma separated values to indicate the amount of items you'd like to use in a string format"
            raise serializers.ValidationError({'message':msg})
        return data

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


class FeedbackQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = (
            'get_feedback_statements',
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


class ResumeProjectDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResumeProjectDetails
        fields = (
            'id',
            'info',
            'resume_project',
        )


class ResumeProjectsSerializer(serializers.ModelSerializer):
    # in addition to the resume project notes, we also need to provide the project details

    """
        Here are some potential problems:
            Related names for serializer?
            resume_project_id??? <-- but we're using functional based view
            query does not exist?? <-- we're not using filter though so...

        Next Steps:
            Could we bullet format the list of info in serializer?
            Test endpoints and functionality for correct API response returns
    """

    resume_proj_details = ResumeProjectDetailsSerializer(many=True, allow_null=True, required=False)
    resume_proj_notes = ProjectNotesSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = ResumeProjects
        fields = (
            'id',
            'project_name',
            'resume_slug',
            'resume',
            'resume_proj_details',
            'resume_proj_notes',
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


class ResumeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(allow_null=True, required=False, read_only=True)
    resume_project = ResumeProjectsSerializer(allow_null=True, required=False, read_only=True, many=True)
    resume_award_achievement = ResumeAwardsAndAchievementsSerializer(allow_null=True, required=False, read_only=True, many=True)
    rel_courses = serializers.SerializerMethodField('get_rel_courses')
    lang = serializers.SerializerMethodField('get_lang')
    fw = serializers.SerializerMethodField('get_fw')
    tools = serializers.SerializerMethodField('get_tools')

    # resume projects?

    def validate(self, data):
        if ', ' not in data.get('school_rel_courses', None) or ', ' not in data.get('skills_lang', None) \
                or ', ' not in data.get('skills_fw', None) or ', ' not in data.get('skills_tools', None):
            msg = "Please use comma separated values to indicate the amount of items you'd like to use in a string format"
            raise serializers.ValidationError({'message':msg})
        return data

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
                  'resume_project',
                  'resume_award_achievement'
        )
