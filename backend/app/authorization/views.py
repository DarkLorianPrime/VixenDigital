from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from authorization.serializers import RegistrationSerializer


class RegistrationViewSet(ModelViewSet):
    serializer_class = RegistrationSerializer


class TokenViewSet(TokenObtainPairView):
    _serializer_class = "authorization.serializers.TokenSerializer"
