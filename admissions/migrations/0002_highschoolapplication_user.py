# Generated by Django 2.2.6 on 2019-10-30 03:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [("admissions", "0001_initial"), ("register", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="highschoolapplication",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="register.Student"
            ),
        )
    ]
