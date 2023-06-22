# Generated by Django 4.1.5 on 2023-06-22 07:29

from django.db import migrations, models
import django.db.models.deletion
import jdwebport_app.models


class Migration(migrations.Migration):

    dependencies = [
        ('jdwebport_app', '0005_quote_author'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resume',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('school_name', models.CharField(max_length=150)),
                ('school_loc', models.CharField(max_length=250)),
                ('school_gpa', models.DecimalField(decimal_places=1, max_digits=2, validators=[jdwebport_app.models.Resume.validate_gpa])),
                ('school_degree', models.CharField(max_length=150)),
                ('school_rel_courses', models.TextField(help_text='Comma Seperated', max_length=500)),
                ('skills_lang', models.TextField(help_text='Comma Seperated', max_length=500)),
                ('skills_fw', models.TextField(help_text='Comma Seperated', max_length=500)),
                ('skills_tools', models.TextField(help_text='Comma Seperated', max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='biography',
            name='profile',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='biography', to='jdwebport_app.profile'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='ResumeProjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=225)),
                ('slug', models.SlugField()),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jdwebport_app.resume')),
            ],
        ),
        migrations.CreateModel(
            name='ResumeAwardsAndAchievements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('award_achievement_name', models.CharField(max_length=150)),
                ('initial_date', models.DateField()),
                ('final_date', models.DateField()),
                ('duration', models.DurationField()),
                ('resume', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jdwebport_app.resume')),
            ],
        ),
    ]
