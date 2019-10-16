# Generated by Django 2.2.6 on 2019-10-16 22:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0003_auto_20191016_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin_Staff',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('email_address', models.EmailField(max_length=200, null=True, validators=[django.core.validators.EmailValidator()])),
                ('phoneNumber', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator("r'^([0-9]{3}) [0-9]{3}-[0-9]{4}$'")])),
                ('username', models.CharField(max_length=20, null=True)),
                ('password', models.CharField(max_length=256)),
                ('school', models.CharField(blank=True, max_length=100, null=True)),
                ('supervisor_email', models.EmailField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
