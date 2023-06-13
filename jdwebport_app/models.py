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


class Profile(models.Model):
    full_name = models.CharField(max_length=100)
    # Quick three words etc description
    quick_description = models.CharField(max_length=100)

    def __str__(self):
        return self.full_name


class SocialsProfile(models.Model):
    """
        social name: The social platform like instagram or github
        info: our username for that social/communicative platform
        info_link: a link to our platform
        info_icon: a Material Design Icon for be placed next to the buttons
        info_color: just the color of the button
    """
    social_name = models.CharField(max_length=50)
    info = models.CharField(max_length=50)
    info_link = models.URLField()
    info_icon = models.CharField(max_length=20)
    info_color = models.CharField(max_length=20)

    # all of these social details are associated with our main profile
    profile = models.ForeignKey(Profile, blank=True, related_name='socials', on_delete=models.CASCADE)

    def __str__(self):
        return self.social_name


class Biography(models.Model):
    # Main bio description
    bio_description = models.TextField(max_length=500, blank=False)
    bio_entry_date = models.DateTimeField(auto_now_add=True)

    # Quote & Author
    quote = models.TextField(max_length=500, blank=False)
    author = models.CharField(max_length=200)

    # current project/activity
    curr_proj_name = models.CharField(max_length=100)
    curr_proj_description = models.TextField(max_length=500)
    curr_proj_entry_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Biographies"

    def get_short_bio_description(self):    # this will be displayed on the front page near "see more"
        return f'{self.bio_description[:100]}...'

    def __str__(self):
        return self.get_short_bio_description()


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

