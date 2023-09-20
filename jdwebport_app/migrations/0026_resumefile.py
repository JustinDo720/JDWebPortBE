# Generated by Django 4.1.5 on 2023-09-19 20:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jdwebport_app', '0025_proj_img_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResumeFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resume_file', models.FileField(upload_to='resume_files/')),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='resume_file', to='jdwebport_app.resume')),
            ],
        ),
    ]
