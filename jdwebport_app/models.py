from django.db import models
from django.utils.text import slugify

# Create your models here.

"""
Safely delete migrations rules:
1) Make sure to makemigrations before this process and be sure that all fixes are in the migrations file
2) Run "python manage.py migrate app_name zero" --> unapply all migrations 
3) Remove pycache from /migrations/__pycache__/ (the pyc that correlates to the migrations you want to delete)
4) Remove the python files from /migrations/ (the py that correlates to the migrations you want to delete)
"""


class Biography(models.Model):
    # Main bio description
    bio_description = models.TextField(max_length=500, blank=False)
    # Quick three words etc description
    quick_description = models.CharField(max_length=100)
    bio_entry_date = models.DateTimeField(auto_now_add=True)

    # current project/activity
    curr_proj_name = models.CharField(max_length=100)
    curr_proj_description = models.TextField(max_length=500)
    curr_proj_entry_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Biographies"

    def __str__(self):
        return self.bio_description[:100]


class Project(models.Model):
    proj_name = models.CharField(max_length=100, blank=False, unique=True, null=False)
    proj_img = models.ImageField(upload_to='project_images/', blank=True, null=True)    # optional
    proj_description = models.TextField(max_length=500)
    # link to github repo
    proj_url = models.URLField(max_length=1000)
    proj_date = models.DateField()
    # showcasing our project
    showcasing = models.BooleanField(default=True)  # turn off old projects
    showcasing_url = models.URLField(max_length=1000)
    # project identifier
    proj_slug = models.SlugField(max_length=100, unique=True, blank=True)   # set blank true because we could set one

    class Meta:
        verbose_name = "Projects"
        ordering = ('-proj_date',)

    def _get_unique_slug(self):
        slug = slugify(self.proj_name)
        unique_slug = slug
        number = 1
        while Project.objects.filter(proj_slug=unique_slug).exists():
            unique_slug = f'{slug}-{number}'
            number += 1
        return unique_slug

    def _get_image_url(self):
        return self.proj_img.url if self.proj_img else None

    def save(self, *args, **kwargs):
        if not self.proj_slug:
            self.proj_slug = self._get_unique_slug()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.proj_name


class ContactMe(models.Model):
    user_email = models.EmailField(max_length=300, blank=False)
    user_first_name = models.CharField(max_length=30, blank=False)
    user_last_name = models.CharField(max_length=30, blank=False)
    user_inquiry = models.TextField(max_length=500, blank=False)
    inquiry_date = models.DateTimeField(auto_now_add=True)
    inquiry_accomplished = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Contact Me"
        ordering = ('inquiry_date',)

    def __str__(self):
        return self.user_inquiry[:20] + " Accomplished: " + str(self.inquiry_accomplished)

