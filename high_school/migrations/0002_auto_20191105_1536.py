# Generated by Django 2.2.6 on 2019-11-05 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("high_school", "0001_initial")]

    operations = [
        migrations.AlterField(
            model_name="highschool",
            name="website",
            field=models.CharField(max_length=70),
        )
    ]