# Generated by Django 3.0.5 on 2020-05-03 13:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20200502_1855'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_premium',
        ),
    ]
