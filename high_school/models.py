from django.db import models


class HighSchool(models.Model):
    dbn = models.CharField(max_length=10, blank=False, null=False)
    school_name = models.CharField(max_length=200, blank=False, null=False)
    boro = models.CharField(max_length=1, blank=False, null=False)
    overview_paragraph = models.CharField(max_length=1000)
    neighborhood = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    school_email = models.EmailField(blank=False, null=False)
    website = models.CharField(max_length=50)
    total_students = models.IntegerField()
    start_time = models.CharField(max_length=6)
    end_time = models.CharField(max_length=6)
