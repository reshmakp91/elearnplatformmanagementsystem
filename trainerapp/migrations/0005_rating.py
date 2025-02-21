# Generated by Django 4.2.16 on 2024-09-27 06:37

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managerapp', '0014_manager'),
        ('trainerapp', '0004_videoprogress'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('review', models.TextField(blank=True, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managerapp.course')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managerapp.student')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managerapp.trainer')),
            ],
        ),
    ]
