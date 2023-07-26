# Generated by Django 4.1.5 on 2023-06-27 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jdwebport_app', '0007_notes_resume'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feedback_option', models.CharField(choices=[('gen', 'General'), ('web', 'Website')], default='gen', max_length=3)),
                ('user_email', models.CharField(max_length=200)),
                ('user_fb_desc', models.TextField(max_length=500)),
                ('user_web_fb_ans', models.CharField(blank=True, max_length=300, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='contactme',
            name='user_files',
            field=models.FileField(blank=True, null=True, upload_to='contact_files/'),
        ),
        migrations.AddField(
            model_name='contactme',
            name='user_purpose',
            field=models.CharField(choices=[('job_opp', 'Job Opportunity'), ('connect', 'Connect With Me'), ('feedback', 'General/Website Feedback')], default='connect', max_length=10),
        ),
    ]
