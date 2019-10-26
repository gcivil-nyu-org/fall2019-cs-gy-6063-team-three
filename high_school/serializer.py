from rest_framework import serializers
from .models import HighSchool


class HighSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighSchool
        fields = '__all__'
