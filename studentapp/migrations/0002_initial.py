# Generated by Django 4.2.16 on 2024-09-22 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('studentapp', '0001_initial'),
        ('trainerapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainerrating',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trainerapp.trainer'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentapp.course'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='purchased_courses',
            field=models.ManyToManyField(to='studentapp.course'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='student',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='purchasedcourse',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='studentapp.course'),
        ),
        migrations.AddField(
            model_name='purchasedcourse',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='course',
            name='trainer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='trainerapp.trainer'),
        ),
    ]
