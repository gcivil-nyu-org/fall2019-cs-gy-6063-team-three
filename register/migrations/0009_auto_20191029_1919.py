# Generated by Django 2.2.6 on 2019-10-29 23:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0008_auto_20191029_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='admin_staff',
            name='email_address',
            field=models.EmailField(max_length=200, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='admin_staff',
            name='username',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='email_address',
            field=models.EmailField(max_length=200, null=True, validators=[django.core.validators.EmailValidator()]),
        ),
        migrations.AlterField(
            model_name='student',
            name='username',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
