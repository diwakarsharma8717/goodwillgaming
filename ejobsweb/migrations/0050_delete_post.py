# Generated by Django 4.0.3 on 2022-08-07 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ejobsweb', '0049_remove_post_user_post_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Post',
        ),
    ]