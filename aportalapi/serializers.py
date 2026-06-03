from django.contrib.auth.models import User
from rest_framework import serializers
from .models import UserUtilities, Chart, Lyrics, SignupSheet


class UserUtilitiesSerializer(serializers.ModelSerializer):
    user_image = serializers.FileField(required=False, allow_null=True)

    class Meta:
        model = UserUtilities
        fields = ['spotify_link', 'apple_link', 'youtube_link', 'user_image']


class UserProfileSerializer(serializers.ModelSerializer):
    utilities = UserUtilitiesSerializer(source='user_utilities', read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'utilities']


class MyProfileSerializer(serializers.ModelSerializer):
    utilities = UserUtilitiesSerializer(source='user_utilities', read_only=True)
    user_image = serializers.FileField(write_only=True, required=False, allow_null=True)
    spotify_link = serializers.URLField(write_only=True, required=False, allow_blank=True)
    apple_link = serializers.URLField(write_only=True, required=False, allow_blank=True)
    youtube_link = serializers.URLField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_superuser', 'utilities',
                  'user_image', 'spotify_link', 'apple_link', 'youtube_link']

    def update(self, instance, validated_data):
        user_image = validated_data.pop('user_image', None)
        spotify_link = validated_data.pop('spotify_link', None)
        apple_link = validated_data.pop('apple_link', None)
        youtube_link = validated_data.pop('youtube_link', None)

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.save()

        utilities, _ = UserUtilities.objects.get_or_create(user=instance)
        if user_image is not None:
            utilities.user_image = user_image
        if spotify_link is not None:
            utilities.spotify_link = spotify_link
        if apple_link is not None:
            utilities.apple_link = apple_link
        if youtube_link is not None:
            utilities.youtube_link = youtube_link
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
        fields = ['id', 'uploaded_by', 'chart_file']


class LyricsSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Lyrics
        fields = ['id', 'uploaded_by', 'lyrics_file']


class SignupSheetSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    user_image = serializers.SerializerMethodField()
    chart_file = serializers.SerializerMethodField()
    lyrics_file = serializers.SerializerMethodField()

    class Meta:
        model = SignupSheet
        fields = [
            'id', 'username', 'first_name', 'last_name', 'user_image',
            'chart', 'chart_file', 'lyrics', 'lyrics_file', 'completed',
        ]
        extra_kwargs = {
            'chart': {'required': False, 'allow_null': True},
            'lyrics': {'required': False, 'allow_null': True},
        }

    def get_user_image(self, obj):
        request = self.context.get('request')
        try:
            image = obj.user.user_utilities.user_image
            if image:
                return request.build_absolute_uri(image.url) if request else image.url
        except Exception:
            pass
        return None

    def get_chart_file(self, obj):
        request = self.context.get('request')
        if obj.chart and obj.chart.chart_file:
            url = obj.chart.chart_file.url
            return request.build_absolute_uri(url) if request else url
        return None

    def get_lyrics_file(self, obj):
        request = self.context.get('request')
        if obj.lyrics and obj.lyrics.lyrics_file:
            url = obj.lyrics.lyrics_file.url
            return request.build_absolute_uri(url) if request else url
        return None
