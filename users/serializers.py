from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from .models import User, Profile, Role


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = ['avatar', 'bio', 'birthdate', 'created_at']
        read_only_fields = ['created_at']


class RegisterSerializer(serializers.ModelSerializer):
    password  = serializers.CharField(
        write_only=True, required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model  = User
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {
            'role': {'required': False}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Las contraseñas no coinciden.'}
            )
        if attrs.get('role') == Role.ADMIN:
            raise serializers.ValidationError(
                {'role': 'No se puede registrar como admin.'}
            )
        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta:
        model  = User
        fields = ['id', 'username', 'email', 'role', 'profile']
        read_only_fields = ['id', 'role']


class UpdateProfileSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model  = User
        fields = ['username', 'profile']

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()
        return instance