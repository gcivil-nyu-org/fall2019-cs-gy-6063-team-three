# Generated by Django 2.2.6 on 2019-12-04 03:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("application", "0006_auto_20191125_2332")]

    operations = [
        migrations.AlterField(
            model_name="highschoolapplication",
            name="program",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="high_school.Program",
                verbose_name="Program",
            ),
        ),
        migrations.AlterField(
            model_name="highschoolapplication",
            name="school",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="app_school",
                to="high_school.HighSchool",
                verbose_name="School",
            ),
        ),
    ]
