# Generated by Django 3.0.2 on 2020-06-10 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0005_auto_20200610_1422'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsletter',
            name='email',
            field=models.ManyToManyField(to='newsletters.NewsletterUser'),
        ),
    ]