from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone', 'email', 'score', 'points', 'is_premium')
        read_only_fields = ('points', 'score')
        extra_kwargs = {
            'phone': {'write_only': True}
        }

    points = serializers.IntegerField(read_only=True)
    score = serializers.FloatField(read_only=True)
    is_premium = serializers.BooleanField(read_only=True)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'profile')
        extra_kwargs = {
            'user': {'required': False},
            'id': {'read_only': True},
            'password': {'write_only': True}
        }

    profile = ProfileSerializer()

    def create(self, validated_data):

        profile_data = validated_data.pop('profile')

        user = User.objects.create_user(
            is_active=False,
            username=validated_data['username'],
            password=validated_data['password'],
        )
        if 'user' in profile_data:
            del profile_data['user']
    
        profile = Profile.objects.create(user=user, **profile_data)

        return user



    def update(self, instance, validated_data):
        profile_update = validated_data.pop('profile', None)

        updated_user = functions.update_instance(instance, validated_data, ('username', 'password'))

        if profile_update:
            updated_user.profile = functions.update_instance(instance.profile, profile_update)
            
        return instance