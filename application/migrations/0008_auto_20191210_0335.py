# Generated by Django 2.2.8 on 2019-12-10 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("application", "0007_auto_20191203_2250")]

    operations = [
        migrations.AlterField(
            model_name="highschoolapplication",
            name="application_number",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="highschoolapplication",
            name="parent_phoneNumber",
            field=models.CharField(
                max_length=15, verbose_name="Parent/Guardian Phone Number"
            ),
        ),
        migrations.AlterField(
            model_name="highschoolapplication",
            name="phoneNumber",
            field=models.CharField(max_length=15, verbose_name="Phone Number"),
        ),
    ]
