# Generated by Django 2.2.6 on 2019-10-29 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='admin_staff',
            name='school_id',
        ),
    ]
