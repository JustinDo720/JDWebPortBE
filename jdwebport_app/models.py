from django.db import models
from django.utils.text import slugify
from django.core.exceptions import ValidationError

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

    # profile link
    profile = models.ForeignKey(Profile, related_name="biography", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Biographies"

    def get_short_bio_description(self):    # this will be displayed on the front page near "see more"
        return f'{self.bio_description[:100]}...'

    def __str__(self):
        return self.get_short_bio_description()


# Recent Projects instead of Current Projects
class CurrProj(models.Model):
    focus_title = models.CharField(max_length=255)
    focus_date = models.DateField()
    focus_info = models.TextField(max_length=500)

    def __str__(self):
        return self.focus_title


class Project(models.Model):
    proj_name = models.CharField(max_length=100, blank=False, unique=True, null=False)
    proj_img = models.ImageField(upload_to='project_images/', blank=True, null=True)    # optional
    proj_description = models.TextField(max_length=500)
    proj_purpose = models.TextField(max_length=500)
    proj_learnings = models.TextField(max_length=700, help_text="Comma Seperated")
    proj_tools = models.CharField(max_length=500, help_text="Comma Seperated")

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

    # method to be used in serializer for learnings and tools field
    def listify_field(self, field):
        return field.split(',')

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
    user_files = models.FileField(upload_to="contact_files/", blank=True, null=True)
    user_inquiry = models.TextField(max_length=500, blank=False)
    inquiry_date = models.DateTimeField(auto_now_add=True)
    inquiry_accomplished = models.BooleanField(default=False)

    # choice field
    PURPOSE_CHOICES = [
        ('job_opp', "Job Opportunity"),
        ('connect', "Connect With Me"),
        ('feedback', "General/Website Feedback"),
    ]
    user_purpose = models.CharField(max_length=10, choices=PURPOSE_CHOICES, default='connect')


    class Meta:
        verbose_name = "Contact Me"
        ordering = ('inquiry_date',)

    def __str__(self):
        return self.user_inquiry[:20] + " Accomplished: " + str(self.inquiry_accomplished)


class Feedback(models.Model):
        """
            Feedback model could fall under two categories:
                General --> overall descriptions / comments for anything (doesn't have to be website related)
                Website --> Q&A / rating / tips etc ... for the website
        """
        # introduce the two options
        FEEDBACK_CHOICES = [
            ('gen', 'General'),
            ('web', 'Website')
        ]
        feedback_option = models.CharField(max_length=3, choices=FEEDBACK_CHOICES, default='gen')

        # either one will include the description and email
        user_email = models.CharField(max_length=200, blank=False, null=False)
        user_fb_desc = models.TextField(max_length=500, blank=False, null=False)  # required
        user_web_fb_ans = models.CharField(max_length=300, blank=True, null=True)


        def get_feedback_statements(self):
            return [
                "The overall layout and organization of my portfolio website is visually appealing.",
                "The navigation on my portfolio website is intuitive and easy to use.",
                "The use of images and multimedia elements on my portfolio website effectively showcases my work.",
                "The responsiveness of my portfolio website ensures a seamless experience across different devices and screen sizes.",
                "The inclusion of relevant information and project details on my portfolio website effectively communicates my skills and expertise."
            ]

        def get_feedback_answers(self):
            # user_web_fb_ans will be a string of comma separated numbers which rep the answers to each question in order
            if self.user_web_fb_ans:
                feedback_answers = []
                answers = self.user_web_fb_ans.split(',')
                for index,statement in enumerate(self.get_feedback_statements()):
                    feedback_answers.append({
                        'question_num': index + 1,
                        'question': self.get_feedback_statements()[index],
                        'user_ans': answers[index]
                    })
                return feedback_answers
            else:
                return []

        def __str__(self):
            return self.user_email


class Resume(models.Model):
    # profile info
    profile = models.ForeignKey(Profile, related_name="resume", on_delete=models.CASCADE)
    # school info
    school_name = models.CharField(max_length=150)
    school_loc = models.CharField(max_length=250)
    # school gpa validator for max gpa

    def validate_gpa(value):
        if value > 4.0 or value < 0:
            return ValidationError
        else:
            return value

    school_gpa = models.DecimalField(max_digits=2, decimal_places=1, validators=[validate_gpa])
    school_degree = models.CharField(max_length=150)
    # we can use a method to return a list based off of commas
    school_rel_courses = models.TextField(max_length=500, help_text="Comma Seperated")

    # skills
    skills_lang = models.TextField(max_length=500, help_text="Comma Seperated")
    skills_fw = models.TextField(max_length=500, help_text="Comma Seperated")
    skills_tools = models.TextField(max_length=500, help_text="Comma Seperated")

    # Projects and Awards and Achievement ForeignKeys but we need to make the methods
    def listify_field(self, field):
        return field.split(',')

    def __str__(self):
        return self.school_name


class ResumeProjects(models.Model):
    project_name = models.CharField(max_length=225)
    slug = models.SlugField()
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return self.project_name


class ResumeAwardsAndAchievements(models.Model):
    award_achievement_name = models.CharField(max_length=150)
    initial_date = models.DateField()
    final_date = models.DateField()
    duration = models.DurationField()
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE)

    def __str__(self):
        return award_achievement_name


class ProjectNotes(models.Model):
    # all possible notes for both our Projects and Resume Projects
    init_notes = models.TextField(max_length=500, blank=True, null=True)
    final_notes = models.TextField(max_length=500, blank=True, null=True)
    project_notes = models.TextField(max_length=700, blank=True, null=True)

    # two different foreign keys with blanks as possible values for us to choose which model to link it to
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="proj_notes",blank=True, null=True)
    resume_project = models.ForeignKey(ResumeProjects, on_delete=models.CASCADE, blank=True, null=True)


    def __str__(self):
        return f"{self.project.proj_name}-{self.id}"