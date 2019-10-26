from django.db import models


class HighSchools(models.Model):
    dbn = models.CharField(max_length=10)
