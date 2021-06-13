from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'photo', 'interests', 'recieve_emails','age', 'gender')
        read_only_fields = ('email', )