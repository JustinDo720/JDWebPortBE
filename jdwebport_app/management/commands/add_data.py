from django.core.management.base import BaseCommand, CommandError
from jdwebport_app.models import Project, Biography, ContactMe, Profile
from jdwebport_app.models import *
from faker import Faker
from faker_education import SchoolProvider
import random



class Command(BaseCommand):
    help = 'Creates a new model instance'

    def add_arguments(self, parser):
        # Required
        parser.add_argument('model', type=str, help="Model name to add data to")
        # optional
        parser.add_argument('-n', '--number', type=int, help='Number of times to add')

    def handle(self, *args, **kwargs):
        model = kwargs['model'].lower()
        try:
            number = kwargs['number']
        except TypeError:
            number = 1 # Default option to create one of everything

        fake = Faker()
        fake.add_provider(SchoolProvider)

        def project_instance():
            # creating a project instance
            """
            Required fields to create project instance:
                {
                    "proj_name": [
                        "This field is required."
                    ],
                    "proj_description": [
                        "This field is required."
                    ],
                    "proj_url": [
                        "This field is required."
                    ],
                    "proj_date": [
                        "This field is required."
                    ],
                    "showcasing_url": [
                        "This field is required."
                    ]
                }
            """
            for num in range(number):
                fake_data = {
                    'date': fake.date(),
                    'url': fake.url(),
                    'desc': fake.paragraph(nb_sentences=10),
                    'text': fake.unique.text(max_nb_chars=20)
                }
                project = Project.objects.create(
                    proj_name=fake_data['text'],
                    proj_description=fake_data['desc'],
                    proj_url=fake_data['url'],
                    proj_date=fake_data['date'],
                    showcasing_url=fake_data['url']
                )
                project.save()
                print(f"{project} created")

        def profile_instance():
            # creating a profile instance
            """
                {
                    "full_name": [
                        "This field is required."
                    ],
                    "quick_description": [
                        "This field is required."
                    ],
                }
            """
            if Profile.objects.count() == 0:
                fake_data = {
                    "full_name": fake.name(),
                    "quick_description": fake.paragraph(nb_sentences=2)
                }
                profile = Profile.objects.create(
                    full_name = fake_data["full_name"],
                    quick_description = fake_data["quick_description"]
                )
                profile.save()
                print(profile)
            else:
                print("Profile Instance already exists")


        def biography_instance():
            # creating a biography instance
            """
            Required fields to create bio instance:
                {
                    "bio_description": [
                        "This field is required."
                    ],
                    "quick_description": [
                        "This field is required."
                    ],
                    "curr_proj_name": [
                        "This field is required."
                    ],
                    "curr_proj_description": [
                        "This field is required."
                    ]
                }
            """

            # but the idea is that we only have 1 biography so
            bio_count = Biography.objects.count()
            latest_profile_id = Profile.objects.latest('id')
            if bio_count < 1:
                fake_data = {
                    'para': fake.paragraph(nb_sentences=10),
                    'desc': fake.paragraph(nb_sentences=3),
                    'text': fake.text(max_nb_chars=20)
                }
                biography = Biography.objects.create(
                    profile = latest_profile_id,
                    bio_description=fake_data['para'],
                    # quick_description=fake_data['desc'],
                    # curr_proj_name=fake_data['text'],
                    # curr_proj_description=fake_data['para']
                )
                biography.save()

        def contactme_instance():
            # creating a contact me instance
            """
            Required fields to create contact me instance:
                {
                    "user_email": [
                        "This field is required."
                    ],
                    "user_first_name": [
                        "This field is required."
                    ],
                    "user_last_name": [
                        "This field is required."
                    ],
                    "user_inquiry": [
                        "This field is required."
                    ]
                }
            """
            for num in range(number):
                fake_data = {
                    'email': fake.email(),
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'desc': fake.paragraph(nb_sentences=10)
                }
                contact = ContactMe.objects.create(
                    user_email=fake_data['email'],
                    user_first_name=fake_data['first_name'],
                    user_last_name=fake_data['last_name'],
                    user_inquiry=fake_data['desc']
                )
                contact.save()

        """
            We need to make a few more instances:
                - Current Projects 
                - Feedbacks 
                - Project Notes 
                - Resume 
                - Resume Awards...
                - Resume Projects 
                - Social Profiles 
        """

        def curr_proj_instance():
            # Creating a Current Project Instance
            """
                {
                    "focus_title": [
                        "This field is required."
                    ],
                    "focus_date": [
                        "This field is required."
                    ],
                    "focus_info": [
                        "This field is required."
                    ]
                }
            """
            for num in range(number):
                faker_data = {
                    'focus_title': fake.unique.job(),
                    'focus_date': fake.date(),
                    'focus_info': fake.paragraph(nb_sentences=5)
                }
                curr_proj = CurrProj.objects.create(
                    focus_title=faker_data['focus_title'],
                    focus_date=faker_data['focus_date'],
                    focus_info=faker_data['focus_info']
                )
                curr_proj.save()
                print(curr_proj, 'has been created')

        def feedback_instance():
            # Creating a Feedback Instance
            """
                {
                    "user_email": [
                        "This field is required."
                    ],
                    "user_fb_desc": [
                        "This field is required."
                    ]
                    "user_web_fb_ans": "5, 2, 4, 5, 1"???
                }
            """
            for num in range(number):
                faker_data = {
                    "user_email": fake.unique.email(),
                    "user_fb_desc": fake.paragraph(nb_sentences=3),
                    "user_web_fb_ans": f'{random.randint(1, 5)}, {random.randint(1, 5)}, {random.randint(1, 5)}, {random.randint(1, 5)}, {random.randint(1, 5)}, '
                }
                fb_instance = Feedback.objects.create(
                    user_email=faker_data['user_email'],
                    user_fb_desc=faker_data['user_fb_desc'],
                    user_web_fb_ans=faker_data['user_web_fb_ans']
                )
                fb_instance.save()
                print(fb_instance, 'sent a feedback')


        def proj_notes_instance():
            # Creating a Project Notes Instance
            """
                {
                    "init_notes": [
                        "optional"
                    ],
                    "finial_notes": [
                        "optional"
                    ],
                    "project_notes": [
                        "This field is required."
                    ]
                    "project": [Not required but we need one or the other],
                    "resume_project": [Not required but we need one or the other],
                }
            """
            proj_ids = [proj_id.id for proj_id in Project.objects.all()]
            resume_proj_ids = [resume_proj_id.id for resume_proj_id in ResumeProjects.objects.all()]


            for num in range(number):
                f_d = {
                    "init_notes": fake.words(nb=6),
                    "final_notes": fake.words(nb=6),
                    "project_notes": fake.paragraph(nb_sentences=4)
                }
                if proj_ids and resume_proj_ids:
                    choice = random.choice(['proj', 'resume_proj'])
                elif proj_ids and not resume_proj_ids:
                    choice = 'proj'
                else:
                    choice = 'resume_proj'


                if choice == 'proj':
                    project_id = random.choice(proj_ids)
                    proj = Project.objects.get(id=project_id)
                    # test if this id already has project notes
                    proj_notes = ProjectNotes.objects.create(
                        init_notes = f_d['init_notes'],
                        final_notes = f_d['final_notes'],
                        project_notes = f_d['project_notes'],
                        project = proj
                    )
                    proj_notes.save()
                else:
                    resume_project_id = random.choice(resume_proj_ids)
                    resume_proj = ResumeProjects.objects.get(id=resume_project_id)
                    resume_proj_notes = ProjectNotes.objects.create(
                        init_notes = f_d['init_notes'],
                        final_notes = f_d['final_notes'],
                        project_notes = f_d['project_notes'],
                        resume_project = resume_proj
                    )
                    resume_proj_notes.save()

        def resume_instance():
            # Creating a Resume Instance
            """
                {
                    "school_name": [
                        "This field is required."
                    ],
                    "school_loc": [
                        "This field is required."
                    ],
                    "school_gpa": [
                        "This field is required."
                    ],
                    "school_degree": [
                        "This field is required."
                    ],
                    "school_rel_courses": [
                        "This field is required."
                    ],
                    "skills_lang": [
                        "This field is required."
                    ],
                    "skills_fw": [
                        "This field is required."
                    ],
                    "skills_tools": [
                        "This field is required."
                    ]
                }
            """
            # only one instance
            if Resume.objects.count() < 1:
                latest_profile_id = Profile.objects.latest('id')
                f_d = {
                    "school_name": fake.school_name(),
                    "school_loc": f'{fake.school_state()}',
                    "school_gpa": fake.pydecimal(left_digits=0, right_digits=2, positive=True) * 4,
                    "school_degree": fake.school_type(),
                    "school_rel_courses": f'{fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}',
                    "skills_lang": f'{fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}',
                    "skills_fw": f'{fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}',
                    "skills_tools": f'{fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}, {fake.text(max_nb_chars=10)}',
                }
                Resume.objects.create(
                    school_name=f_d['school_name'],
                    school_loc=f_d['school_loc'],
                    school_gpa=f_d['school_gpa'],
                    school_degree=f_d['school_degree'],
                    school_rel_courses=f_d['school_rel_courses'],
                    skills_lang=f_d['skills_lang'],
                    skills_fw=f_d['skills_fw'],
                    skills_tools=f_d['skills_tools'],
                    profile=latest_profile_id
                )
            else:
                print("Resume instance already exists")

        def resume_awards_instance():
            # Creating a Resume Awards Instance
            """
                {
                    "award_achievement_name": [
                        "This field is required."
                    ],
                    "initial_date": [
                        "This field is required."
                    ],
                    "final_date": [
                        "This field is required."
                    ]
                }
            """
            resume = Resume.objects.latest('id')
            if Resume.objects.count() == 1:

                for num in range(number):
                    f_d = {
                        'award_achievement_name': fake.text(max_nb_chars=20),
                        'initial_date': fake.date(),
                        'final_date': fake.date()
                    }

                    resume_award = ResumeAwardsAndAchievements.objects.create(
                        award_achievement_name=f_d['award_achievement_name'],
                        initial_date=f_d['initial_date'],
                        final_date=f_d['final_date'],
                        resume= resume
                    )

                    resume_award.save()
            else:
                print('Create Resume before adding awards')
                resume_instance()
                resume_awards_instance()


        def resume_projects_instance():
            # Creating a Resume Projects Instance
            """
            {
                "project_name": "required",
                "slug": "required"
            }
            """
            if Resume.objects.count() == 1:
                resume = Resume.objects.latest('id')
                for num in range(number):
                    f_d = {
                        "project_name": fake.text(max_nb_chars=10),
                        "slug": fake.text(max_nb_chars=6)
                    }
                    resume_proj = ResumeProjects.objects.create(
                        project_name=f_d["project_name"],
                        resume_slug=f_d["slug"],
                        resume=resume
                    )
                    resume_proj.save()
            else:
                print("Create Resume Instance first before Resume Project Instances")
                resume_instance()
                resume_projects_instance()


        def social_profiles_instance():
            # Creating a Social Profiles Instance
            """
                {
                    "social_name": "github",
                    "info": "Info session",
                    "info_link": "https://www.wizard101central.com/wiki/Creature:King_Detritus",
                    "info_icon": "github",
                    "info_color": "blue"
                }
            """
            if Profile.objects.count() == 1:
                profile = Profile.objects.latest('id')
                for num in range(number):
                    f_d = {
                        "social_name": fake.text(max_nb_chars=5),
                        "info": fake.paragraph(nb_sentences=1),
                        "info_link": "https://www.wizard101central.com/wiki/Creature:King_Detritus",
                        "info_icon": fake.text(max_nb_chars=5),
                        "info_color": fake.text(max_nb_chars=5)
                    }

                    social_insance = SocialsProfile.objects.create(
                        social_name=f_d["social_name"],
                        info=f_d["info"],
                        info_link=f_d["info_link"],
                        info_icon=f_d["info_icon"],
                        info_color=f_d["info_color"],
                        profile = profile
                    )
                    social_insance.save()
                    print(social_insance)
                print('Disregard the error. %s more social instances have been created' % str(number))


        if 'proj' in model and 'curr' not in model and 'notes' not in model and 'resume' not in model:
            project_instance()
        elif 'resume' in model and 'proj' in model:
            resume_projects_instance()
        elif 'profile' in model and 'social' not in model:
            profile_instance()
        elif 'bio' in model:
            biography_instance()
        elif 'contact' in model:
            contactme_instance()
        elif 'curr' in model:
            curr_proj_instance()
        elif 'resume' in model and 'proj' not in model and 'awards' not in model:
            resume_instance()
        elif 'feedback' in model:
            feedback_instance()
        elif 'notes' in model:
            proj_notes_instance()
        elif 'awards' in model:
            resume_awards_instance()
        elif 'social' in model:
            social_profiles_instance()
        elif 'all' in model:
            # build all models
            profile_instance()
            resume_instance()
            project_instance()
            biography_instance()
            contactme_instance()
            curr_proj_instance()
            feedback_instance()
            proj_notes_instance()
            resume_awards_instance()
            resume_projects_instance()
            social_profiles_instance()