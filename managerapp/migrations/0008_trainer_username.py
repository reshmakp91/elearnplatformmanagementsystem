# Generated by Django 4.2.16 on 2024-09-23 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerapp', '0007_alter_trainer_password_alter_trainer_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainer',
            name='username',
            field=models.CharField(max_length=100, null=True),
        ),
    ]