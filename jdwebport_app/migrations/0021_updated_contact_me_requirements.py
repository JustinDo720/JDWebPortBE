# Generated by Django 4.1.5 on 2023-08-22 16:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdwebport_app', '0020_alter_biographysection_biography_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactme',
            name='user_first_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='contactme',
            name='user_last_name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]