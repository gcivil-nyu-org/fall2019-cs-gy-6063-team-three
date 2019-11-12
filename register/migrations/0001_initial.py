import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import register.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [("high_school", "0001_initial")]

    operations = [
        migrations.CreateModel(
            name="Student",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "email_address",
                    models.EmailField(
                        max_length=200,
                        null=True,
                        validators=[
                            django.core.validators.EmailValidator(),
                            register.validators.validate_not_used_student_email,
                        ],
                    ),
                ),
                (
                    "phoneNumber",
                    models.CharField(
                        max_length=15,
                        validators=[
                            django.core.validators.RegexValidator(
                                "r'^([0-9]{3}) [0-9]{3}-[0-9]{4}$'"
                            )
                        ],
                    ),
                ),
                ("username", models.CharField(max_length=20, null=True)),
                ("password", models.CharField(max_length=256)),
                ("is_active", models.BooleanField(default=False)),
                (
                    "current_school",
                    models.CharField(blank=True, max_length=100, null=True),
                ),
                ("borough", models.CharField(max_length=2)),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Admin_Staff",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(blank=True, max_length=50, null=True)),
                ("last_name", models.CharField(blank=True, max_length=50, null=True)),
                (
                    "email_address",
                    models.EmailField(
                        max_length=200,
                        null=True,
                        validators=[
                            django.core.validators.EmailValidator(),
                            register.validators.validate_not_used_admin_email,
                        ],
                    ),
                ),
                (
                    "phoneNumber",
                    models.CharField(
                        max_length=15,
                        validators=[
                            django.core.validators.RegexValidator(
                                "r'^([0-9]{3}) [0-9]{3}-[0-9]{4}$'"
                            )
                        ],
                    ),
                ),
                ("username", models.CharField(max_length=20, null=True)),
                ("password", models.CharField(max_length=256)),
                ("is_active", models.BooleanField(default=False)),
                ("is_verified_employee", models.BooleanField(default=False)),
                (
                    "supervisor_email",
                    models.EmailField(blank=True, max_length=100, null=True),
                ),
                (
                    "school",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="high_school.HighSchool",
                    ),
                ),
            ],
            options={"abstract": False},
        ),
    ]
