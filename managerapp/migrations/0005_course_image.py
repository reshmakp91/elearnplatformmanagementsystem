# Generated by Django 4.2.16 on 2024-09-22 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerapp', '0004_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(default='default_image.jpg', upload_to='course_images/'),
        ),
    ]
