from django.core.management.base import BaseCommand, CommandError
from jdwebport_app.models import *


class Command(BaseCommand):
    help = 'Remove ALL instances in said model'

    def add_arguments(self, parser):
        # Required
        parser.add_argument('model', type=str, help="Model name to delete all instances")

    def handle(self, *args, **options):
        model = options['model'].lower()
        if 'proj' in model and 'curr' not in model and 'notes' not in model and 'resume' not in model:
            Project.objects.all().delete()
            print("Removed Project")
        elif 'resume' in model and 'proj' in model:
            ResumeProjects.objects.all().delete()
            print("Removed Resume Project")
        elif 'profile' in model and 'social' not in model:
            Profile.objects.all().delete()
            print("Removed Profile")
        elif 'bio' in model:
            Biography.objects.all().delete()
            print("Removed Bio")
        elif 'contact' in model:
            ContactMe.objects.all().delete()
            print("Removed ContactMes")
        elif 'curr' in model:
            CurrProj.objects.all().delete()
            print("Removed Curr Project")
        elif 'resume' in model and 'proj' not in model and 'awards' not in model:
            Resume.objects.all().delete()
            print("Removed Resume")
        elif 'feedback' in model:
            Feedback.objects.all().delete()
            print("Removed Feedbacks")
        elif 'notes' in model:
            ProjectNotes.objects.all().delete()
            print("Removed Project Notes")
        elif 'awards' in model:
            ResumeAwardsAndAchievements.objects.all().delete()
            print("Removed Resume Awards")
        elif 'social' in model:
            SocialsProfile.objects.all().delete()
            print("Removed Socials")
        elif 'all' in model:
            # build all models
            Project.objects.all().delete()
            Profile.objects.all().delete()
            Biography.objects.all().delete()
            ContactMe.objects.all().delete()
            CurrProj.objects.all().delete()
            Resume.objects.all().delete()
            Feedback.objects.all().delete()
            ProjectNotes.objects.all().delete()
            ResumeAwardsAndAchievements.objects.all().delete()
            SocialsProfile.objects.all().delete()
            ResumeProjects.objects.all().delete()
