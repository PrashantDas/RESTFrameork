from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class MemberRegisterSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name  = serializers.CharField()
    username   = serializers.CharField()
    password   = serializers.CharField()

    def validate(self, data):
        data_username = data['username']
        if User.objects.filter(username__iexact=data_username).exists():
            raise serializers.ValidationError(detail='The username alrady exists')
        else:
            return data
        
    def create(self, validated_data):
        making_user = User.objects.create(first_name = validated_data['first_name'],
                            last_name = validated_data['last_name'],
                            username = validated_data['username'])
        making_user.set_password(validated_data['password'])
        making_user.save()
        return validated_data


class MemberLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        if User.objects.filter(username__exact=attrs['username']).exists():
            return attrs
        else:
            raise serializers.ValidationError(detail='User does not exist')
        
    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'id']

