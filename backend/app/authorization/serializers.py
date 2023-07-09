import re

from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import update_last_login
from django.core.validators import RegexValidator
from django.db.models import Q
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt import exceptions
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings

from authorization.models import User

username_validator = RegexValidator(r"^[a-zA-Z0-9_\-]{3,16}$")
password_validator = RegexValidator(r"^.*(?=.{8,32})(?=.*[a-zA-Z])(?=.*\d)(?=.*[!#$%@&?\"]).*$")


class UserSerializer(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "middle_name", "username")


class RegistrationSerializer(ModelSerializer):
    username = serializers.CharField(required=True, validators=[username_validator])
    email = serializers.EmailField(required=True)
    double_password = serializers.CharField(validators=[password_validator], required=True, write_only=True)
    password = serializers.CharField(min_length=8, max_length=128, required=True,
                                     validators=[password_validator], write_only=True)
    first_name = serializers.CharField(min_length=3, required=True)
    last_name = serializers.CharField(min_length=3, required=True)
    middle_name = serializers.CharField(min_length=3, required=False)
    is_superuser = serializers.BooleanField(read_only=True)

    def validate(self, attrs):
        if not attrs["password"] == attrs.get("double_password"):
            raise ValidationError(detail="password and double password is not equal", code=400)

        if self.Meta.model.objects.filter(Q(username=attrs["username"]) | Q(email=attrs["email"])).exists():
            raise ValidationError(detail="this email or username already exists", code=400)

        return attrs

    class Meta:
        model = get_user_model()
        fields = ("username", "password", "double_password", "email", "first_name",
                  "last_name", "middle_name", "is_superuser")

    def create(self, validated_data):
        return self.Meta.model.objects.create_user(**validated_data)


class TokenSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs[self.username_field]
        authenticate_kwargs = {
            "password": attrs["password"],
        }

        if re.search(r"^\S+@\S+\.\S+$", username):
            username = User.objects.filter(email=username).first().username

        authenticate_kwargs["username"] = username

        try:
            authenticate_kwargs["request"] = self.context["request"]
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)
        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"],
                "no_active_account",
            )

        refresh = self.get_token(self.user)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return {"refresh": str(refresh), "access": str(refresh.access_token)}