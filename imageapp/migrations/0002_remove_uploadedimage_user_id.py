# Generated by Django 4.2.1 on 2023-05-15 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('imageapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='uploadedimage',
            name='user_id',
        ),
    ]
