# Generated by Django 3.0.2 on 2020-06-13 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0020_auto_20200613_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.ManyToManyField(to='newsletters.NewsletterUser'),
        ),
    ]
