# Generated by Django 2.2.6 on 2019-10-26 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("high_school", "0002_auto_20191026_1616")]

    operations = [
        migrations.AlterField(
            model_name="highschool",
            name="end_time",
            field=models.CharField(max_length=5),
        ),
        migrations.AlterField(
            model_name="highschool",
            name="location",
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name="highschool",
            name="phone_number",
            field=models.CharField(max_length=15),
        ),
        migrations.AlterField(
            model_name="highschool",
            name="start_time",
            field=models.CharField(max_length=5),
        ),
    ]
