# Generated by Django 4.0.3 on 2022-03-25 04:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ejobsweb', '0004_alter_post_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='post',
            name='like',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user',
        ),
    ]