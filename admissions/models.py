from django.db import models


def auto_str(cls):
    def __str__(self):
        return "%s(%s)" % (
            type(self).__name__,
            ", ".join("%s=%s" % item for item in vars(self).items()),
        )

    cls.__str__ = __str__
    return cls


@auto_str
class Application(models.Model):
    application_id = models.IntegerField(null=True, blank=True)
    first_name = models.CharField(max_length=50, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    program_name = models.CharField(max_length=50, null=True, blank=True)
    date_of_submission = models.DateField("Data of submission")
