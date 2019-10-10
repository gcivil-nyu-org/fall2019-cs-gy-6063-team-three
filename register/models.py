# Create your models here.

from django.db import models


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls

@auto_str
class User(models.Model):
    username = models.CharField(max_length=20, null = True, blank = False)
    first_name = models.CharField(max_length=50, null = True, blank = True)
    last_name = models.CharField(max_length=50, null = True, blank = True)
    email_address = models.CharField(max_length=200, null = True, blank = False)
    current_school = models.CharField(max_length=100, null = True, blank = True)
    borough = models.CharField(max_length=20)
    password = models.CharField(max_length=256)

