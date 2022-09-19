# Generated by Django 4.0.3 on 2022-04-01 07:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ejobsweb', '0022_delete_likebutton'),
    ]

    operations = [
        migrations.CreateModel(
            name='Room2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reciever', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_reciever', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=1000000)),
                ('date', models.DateTimeField(blank=True, default=django.utils.timezone.now)),
                ('user', models.CharField(max_length=1000000)),
                ('Room2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ejobsweb.room2')),
            ],
        ),
    ]
