from rest_framework import serializers

from apps.school.models import School


class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            'school_id', 'name', 'slug', 'logo', 'domain', 'gps_address',
            'phone_number', 'created_at'
        )