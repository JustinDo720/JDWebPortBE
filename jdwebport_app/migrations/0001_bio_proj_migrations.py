# Generated by Django 4.1.5 on 2023-01-04 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Biography',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio_description', models.TextField(max_length=500)),
                ('quick_description', models.CharField(max_length=100)),
                ('bio_entry_date', models.DateTimeField(auto_now_add=True)),
                ('curr_proj_name', models.CharField(max_length=100)),
                ('curr_proj_description', models.TextField(max_length=500)),
                ('curr_proj_entry_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Biographies',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proj_name', models.CharField(max_length=100, unique=True)),
                ('proj_img', models.ImageField(blank=True, upload_to='project_images/')),
                ('proj_description', models.TextField(max_length=500)),
                ('proj_url', models.URLField(max_length=1000)),
                ('proj_date', models.DateField()),
                ('showcasing', models.BooleanField(default=True)),
                ('showcasing_url', models.URLField(max_length=1000)),
                ('proj_slug', models.SlugField(blank=True, max_length=100, unique=True)),
            ],
            options={
                'verbose_name': 'Projects',
                'ordering': ('-proj_date',),
            },
        ),
    ]
