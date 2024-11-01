# Generated by Django 4.2.16 on 2024-09-26 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managerapp', '0013_order'),
    ]

    operations = [
        migrations.CreateModel(
            name='manager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('username', models.CharField(max_length=100, null=True, unique=True)),
                ('password', models.CharField(max_length=128, null=True)),
                ('type', models.CharField(max_length=100, null=True)),
            ],
        ),
    ]
