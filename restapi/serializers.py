#serializers
from rest_framework import serializers

from users.models import User
from .models import Destination, Trip, Interest

#User
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'age', 'gender', 'interests', 'company', 'recieve_emails']

class UserAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['age', 'gender', 'recieve_emails']


#Destination
class DestinationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Destination
        fields = ('destination_id', 'trip_id', 'postal_code', 'name', 'country', 'country_code', 'date_from', 'date_to', 'budget', 'n', 'e')

#Trip
class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields = ('trip_id', 'user_id', 'name', 'description')


class InterestsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interest
        fields = ('interest_id', 'interest')
