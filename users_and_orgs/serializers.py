from rest_framework import serializers

from users_and_orgs.models import CustomUser, Organization


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    is_staff = serializers.BooleanField(read_only=True)
    last_login = serializers.DateTimeField(read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    date_joined = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "url",
            "id",
            "email",
            "password",
            "last_name",
            "first_name",
            "phone",
            "avatar",
            "organizations",
            "is_staff",
            "last_login",
            "is_active",
            "date_joined",
        ]

    def create(self, validated_data):
        """set password to user on creation"""
        user = super().create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

    def update(self, instance, validated_data):
        """update user password if specified"""
        user = super().update(instance, validated_data)
        try:
            user.set_password(validated_data["password"])
            user.save()
        except KeyError:
            pass
        return user


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "id",
            "name",
            "short_description",
            "employees",
        ]
