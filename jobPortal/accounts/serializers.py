from rest_framework import serializers
from .models import *

class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, style={'input_type': 'password'})

    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'profile_photo', 'dob', 'short_bio', 'job_title', 
                  'gender', 'country', 'open_to_hiring', 'password1', 'password2']
    
    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError({"password": "The two password fields didn't match."})
        return data

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['email']
        )
        user.set_password(validated_data['password1'])
        user.save()
        return user
    