# Generated by Django 2.2.6 on 2019-11-13 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("application", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="highschoolapplication",
            name="application_status",
            field=models.CharField(default="pending", max_length=10),
        )
    ]
