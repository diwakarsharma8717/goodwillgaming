# Generated by Django 4.0.3 on 2022-04-01 13:01

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ejobsweb', '0024_rename_room2_message_room'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Room2',
            new_name='Room',
        ),
    ]
