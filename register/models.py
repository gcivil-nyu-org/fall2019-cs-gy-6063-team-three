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
class Register(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.CharField(max_length=200)
    current_school = models.CharField(max_length=100)
    borough = models.CharField(max_length=20)
    password = models.CharField(max_length=8)

