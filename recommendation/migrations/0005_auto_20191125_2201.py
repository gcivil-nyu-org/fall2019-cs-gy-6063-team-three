# Generated by Django 2.2.6 on 2019-11-26 03:01

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("recommendation", "0004_recommendation_rating_comment")]

    operations = [
        migrations.AlterField(
            model_name="recommendation",
            name="email_address",
            field=models.EmailField(
                max_length=50,
                validators=[django.core.validators.EmailValidator()],
                verbose_name="Email Address",
            ),
        ),
        migrations.AlterField(
            model_name="recommendation",
            name="first_name",
            field=models.CharField(max_length=50, verbose_name="First Name"),
        ),
        migrations.AlterField(
            model_name="recommendation",
            name="known_length",
            field=models.IntegerField(null=True, verbose_name="Years"),
        ),
        migrations.AlterField(
            model_name="recommendation",
            name="last_name",
            field=models.CharField(max_length=50, verbose_name="Last Name"),
        ),
        migrations.AlterField(
            model_name="recommendation",
            name="rating_comment",
            field=models.TextField(null=True, verbose_name="Enter your comments here."),
        ),
    ]
