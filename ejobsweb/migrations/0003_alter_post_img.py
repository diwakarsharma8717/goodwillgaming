# Generated by Django 4.0.3 on 2022-03-23 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ejobsweb', '0002_post_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='img',
            field=models.ImageField(default=None, upload_to='<django.db.models.fields.related.ForeignKey> posts'),
        ),
    ]