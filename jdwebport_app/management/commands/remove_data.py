from django.core.management.base import BaseCommand, CommandError
from jdwebport_app.models import Project, Biography, ContactMe


class Command(BaseCommand):
    help = 'Remove ALL instances in said model'

    def add_arguments(self, parser):
        # Required
        parser.add_argument('model', type=str, help="Model name to delete all instances")

    def handle(self, *args, **options):
        model = options['model'].lower()
        if 'proj' in model:
            Project.objects.all().delete()
        elif 'bio' in model:
            Biography.objects.all().delete()
        elif 'contact' in model:
            ContactMe.objects.all().delete()
        elif 'all' in model:
            Project.objects.all().delete()
            Biography.objects.all().delete()
            ContactMe.objects.all().delete()
