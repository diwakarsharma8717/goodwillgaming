# Generated by Django 4.0.3 on 2022-08-06 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ejobsweb', '0047_education'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='img',
            field=models.ImageField(default=None, null=True, upload_to='education_img'),
        ),
    ]