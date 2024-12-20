# Generated by Django 2.2.28 on 2024-06-20 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_auto_20240620_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('club_president', 'Club President'), ('student', 'Student'), ('faculty', 'Faculty')], max_length=20),
        ),
    ]
