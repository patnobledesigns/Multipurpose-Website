# Generated by Django 3.0.2 on 2020-06-08 18:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageSlide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thumbnail', models.URLField(blank=True, max_length=1000, null=True)),
                ('title', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=1000)),
                ('Tagname', models.CharField(blank=True, default='Movie', max_length=200, null=True)),
                ('star', models.CharField(blank=True, max_length=500, null=True)),
                ('genre', models.CharField(blank=True, max_length=500, null=True)),
                ('overview', models.TextField(blank=True, null=True, unique=True)),
                ('release_date', models.CharField(blank=True, max_length=100, null=True)),
                ('language', models.CharField(blank=True, max_length=200, null=True)),
                ('runtime', models.CharField(blank=True, max_length=100, null=True)),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('thumbnail', models.URLField(blank=True, max_length=1000, null=True)),
                ('imdb', models.URLField(blank=True, max_length=500, null=True)),
                ('download_link', models.URLField(blank=True, max_length=800, null=True, unique=True)),
                ('iframe', models.CharField(blank=True, max_length=1000, null=True)),
                ('source', models.CharField(blank=True, max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('rating', models.FloatField(default=0)),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='movies.Movie')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
