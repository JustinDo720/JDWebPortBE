# Generated by Django 4.1.5 on 2023-09-04 06:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdwebport_app', '0023_resumeprojectdetails'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='proj_brief_description',
            field=models.TextField(default='Default brief Description', max_length=300),
            preserve_default=False,
        ),
    ]
