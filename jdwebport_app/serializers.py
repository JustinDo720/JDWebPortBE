# We are going to make some serializers for our front-end
from rest_framework import serializers
from .models import *   # importing all models


class BiographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Biography
        fields = '__all__'


class SocialsProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialsProfile
        fields = '__all__'


class ProfileSerializer(serializers.ModelSerializer):
    socials = SocialsProfileSerializer(many=True)
    biography = BiographySerializer(many=True)

    class Meta:
        model = Profile
        fields = ('full_name', 'quick_description', 'socials', 'biography')


class ProjectSerializer(serializers.ModelSerializer):
    proj_img_url = serializers.SerializerMethodField('get_proj_img_url')
    proj_notes = serializers.SerializerMethodField('get_proj_notes')

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
        )

    def get_proj_img_url(self, obj):
        return obj._get_image_url()

    def get_proj_notes(self, obj):
        return obj.projectnotes_set.all()


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


class ResumeSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
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
        fields = ('profile',
                  'school_name',
                  'school_loc',
                  'school_gpa',
                  'school_degree',
                  'rel_courses',
                  'lang',
                  'fw',
                  'tools',
        )