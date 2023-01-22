# We are going to make some serializers for our front-end
from rest_framework import serializers
from .models import *   # importing all models


class BiographySerializer(serializers.ModelSerializer):
    class Meta:
        model = Biography
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    proj_img_url = serializers.SerializerMethodField('get_proj_img_url')

    class Meta:
        model = Project
        fields = (
            'id',
            'proj_name',
            'proj_img',
            'proj_img_url',
            'proj_description',
            'proj_url',
            'proj_date',
            'showcasing',
            'showcasing_url',
            'proj_slug',
        )

    def get_proj_img_url(self, obj):
        return obj._get_image_url()


class ContactMeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMe
        fields = "__all__"