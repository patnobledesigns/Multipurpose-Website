# Generated by Django 3.0.2 on 2020-05-30 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_review_date_posted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='average_rating',
        ),
    ]
