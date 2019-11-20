# Generated by Django 2.2.6 on 2019-11-20 05:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("recommendation", "0002_auto_20191113_0324")]

    operations = [
        migrations.RemoveField(model_name="recommendation", name="recommendation"),
        migrations.AddField(
            model_name="recommendation",
            name="known_length",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="known_location",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="known_strength",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_analyzing",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_concepts",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_creativity",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_goals",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_mathematical",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_oral",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_socialization",
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name="recommendation",
            name="rating_written",
            field=models.IntegerField(null=True),
        ),
    ]
