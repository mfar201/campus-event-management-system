# Generated by Django 2.2.28 on 2024-06-20 13:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20240620_1335'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='points',
        ),
    ]
