# Generated by Django 2.2.6 on 2019-11-26 00:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("recommendation", "0003_auto_20191120_0038")]

    operations = [
        migrations.AddField(
            model_name="recommendation",
            name="rating_comment",
            field=models.TextField(null=True),
        )
    ]
