# Generated by Django 4.1.5 on 2023-07-21 22:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdwebport_app', '0010_proj_remastered'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='proj_learnings',
            field=models.TextField(help_text='Comma Seperated', max_length=700),
        ),
        migrations.AlterField(
            model_name='project',
            name='proj_tools',
            field=models.CharField(help_text='Comma Seperated', max_length=500),
        ),
    ]
