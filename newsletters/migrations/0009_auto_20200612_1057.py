# Generated by Django 3.0.2 on 2020-06-12 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0008_auto_20200610_2106'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.ManyToManyField(to='newsletters.NewsletterUser'),
        ),
    ]
