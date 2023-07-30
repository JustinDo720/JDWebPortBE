from django.core.management.base import BaseCommand, CommandError
from jdwebport_app.models import Project, Biography, ContactMe, Profile
from jdwebport_app.models import *
from faker import Faker


class Command(BaseCommand):
    help = 'Creates a new model instance'

    def add_arguments(self, parser):
        # Required
        parser.add_argument('model', type=str, help="Model name to add data to")
        # optional
        parser.add_argument('-n', '--number', type=int, help='Number of times to add')

    def handle(self, *args, **kwargs):
        model = kwargs['model'].lower()
        number = kwargs['number']

        fake = Faker()

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
            fake_data = {
                "full_name": fake.name(),
                "quick_description": fake.paragraph(nb_sentences=2)
            }
            profile = Profile.objects.create(
                full_name = fake_data["full_name"],
                quick_description = fake_data["quick_description"]
            )
            profile.save()


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
            if bio_count < 1:
                fake_data = {
                    'para': fake.paragraph(nb_sentences=10),
                    'desc': fake.paragraph(nb_sentences=3),
                    'text': fake.text(max_nb_chars=20)
                }
                biography = Biography.objects.create(
                    profile = Profile.objects.first(),
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

            def proj_notes_instance():
                # Creating a Project Notes Instance
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

            def resume_instance():
                # Creating a Resume Instance
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

            def resume_awards_instance():
                # Creating a Resume Awards Instance
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

            def resume_projects_instance():
                # Creating a Resume Projects Instance
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

            def social_profiles_instance():
                # Creating a Social Profiles Instance
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
        if 'proj' in model:
            project_instance()
        elif 'profile' in model:
            profile_instance()
        elif 'bio' in model:
            biography_instance()
        elif 'contact' in model:
            contactme_instance()
        elif 'all' in model:
            # build all models
            profile_instance()
            project_instance()
            biography_instance()
            contactme_instance()
