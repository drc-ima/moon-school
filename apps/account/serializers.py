from rest_framework import serializers

from apps.account.models import *


class UserSerializer(serializers.ModelSerializer):

    user_type_display = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'account_id', 'school_id', 'first_name', 'middle_name',
            'last_name', 'is_active', 'slug', 'uuid', 'date_joined',
            'user_type', 'user_type_display'
        )

    def get_user_type_display(self, obj):
        return obj.get_user_type_display()
