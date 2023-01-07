from django.contrib import admin
from .models import *

# Register your models here.

our_models = [
    Biography,
    Project,
    ContactMe
]

admin.site.register(model for model in our_models)
