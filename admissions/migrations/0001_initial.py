# Generated by Django 2.2.6 on 2019-10-29 20:53

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('register', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HighSchoolApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('application_number', models.IntegerField()),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email_address', models.EmailField(max_length=50, validators=[django.core.validators.EmailValidator()])),
                ('phoneNumber', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator("r'^([1-9]{1}\\d{2}) \\d{3} -\\d{4}'")])),
                ('address', models.CharField(max_length=100)),
                ('gender', models.CharField(max_length=15)),
                ('date_of_birth', models.DateField()),
                ('gpa', models.DecimalField(decimal_places=2, max_digits=3)),
                ('parent_name', models.CharField(max_length=100)),
                ('parent_phoneNumber', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator("r'^([1-9]{1}\\d{2}) \\d{3} -\\d{4}'")])),
                ('school_id', models.CharField(max_length=100)),
                ('program', models.CharField(max_length=100)),
                ('submitted_date', models.DateTimeField(default=datetime.datetime.now)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='register.Student')),
            ],
        ),
    ]
