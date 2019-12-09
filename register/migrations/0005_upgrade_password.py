from django.db import migrations
from django.contrib.auth.hashers import make_password


# for updating the current passwords to pbkdf2 algorithm
def forwards_func(apps, schema_editor):
    Students = apps.get_model('register', 'Student')
    student_users = Students.objects.exclude(password__startswith="pbkdf2_")
    for user in student_users:
        user.password = make_password(user.password)
        user.save(update_fields=['password'])

    Admin_Staff = apps.get_model('register', 'Admin_Staff')
    admin_staff_users = Admin_Staff.objects.exclude(password__startswith="pbkdf2_")
    for user in admin_staff_users:
        user.password = make_password(user.password)
        user.save(update_fields=['password'])


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_merge_20191113_1332'),
    ]

    operations = [
        migrations.RunPython(forwards_func),
    ]