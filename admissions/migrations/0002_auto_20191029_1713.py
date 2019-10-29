# Generated by Django 2.2.6 on 2019-10-29 21:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [("high_school", "0001_initial"), ("admissions", "0001_initial")]

    operations = [
        migrations.RenameField(
            model_name="highschoolapplication", old_name="user_id", new_name="user"
        ),
        migrations.RemoveField(model_name="highschoolapplication", name="school_id"),
        migrations.AddField(
            model_name="highschoolapplication",
            name="school",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                to="high_school.HighSchool",
            ),
            preserve_default=False,
        ),
    ]
