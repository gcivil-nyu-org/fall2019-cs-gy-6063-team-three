# Generated by Django 2.2.7 on 2019-11-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("application", "0002_auto_20191104_1623")]

    operations = [
        migrations.AlterField(
            model_name="highschoolapplication",
            name="application_number",
            field=models.CharField(max_length=150),
        )
    ]