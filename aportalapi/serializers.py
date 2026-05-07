from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserUtilities, Chart, SignupSheet


class UserUtilitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserUtilities
        fields = ['spotify_link', 'apple_link', 'youtube_link', 'user_image']


class UserProfileSerializer(serializers.ModelSerializer):
    utilities = UserUtilitiesSerializer(source='user_utilities', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'utilities']


class MyProfileSerializer(serializers.ModelSerializer):
    utilities = UserUtilitiesSerializer(source='user_utilities')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'utilities']

    def update(self, instance, validated_data):
        utilities_data = validated_data.pop('user_utilities', {})
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        utilities, _ = UserUtilities.objects.get_or_create(user=instance)
        for attr, value in utilities_data.items():
            setattr(utilities, attr, value)
        utilities.save()

        return instance


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    spotify_link = serializers.URLField(required=False, allow_blank=True)
    apple_link = serializers.URLField(required=False, allow_blank=True)
    youtube_link = serializers.URLField(required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name',
                  'spotify_link', 'apple_link', 'youtube_link']
        extra_kwargs = {
            'email': {'required': False, 'allow_blank': True},
            'first_name': {'required': False, 'allow_blank': True},
            'last_name': {'required': False, 'allow_blank': True},
        }

    def create(self, validated_data):
        spotify_link = validated_data.pop('spotify_link', '')
        apple_link = validated_data.pop('apple_link', '')
        youtube_link = validated_data.pop('youtube_link', '')

        user = User.objects.create_user(**validated_data)

        user.user_utilities.spotify_link = spotify_link
        user.user_utilities.apple_link = apple_link
        user.user_utilities.youtube_link = youtube_link
        user.user_utilities.save()

        return user


class ChartSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Chart
        fields = ['id', 'uploaded_by', 'chart_image']


class SignupSheetSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    chart_image = serializers.ReadOnlyField(source='chart.chart_image.url')

    class Meta:
        model = SignupSheet
        fields = ['id', 'username', 'chart', 'chart_image', 'completed']
