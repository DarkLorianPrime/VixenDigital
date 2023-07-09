from django.db.models import QuerySet
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView

from authorization.models import User
from authorization.serializers import RegistrationSerializer, UserSerializer
from authorization.service import Service

service = Service()


class RegistrationViewSet(ModelViewSet):
    serializer_class = RegistrationSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request: Request, *args, **kwargs):
        user: User = request.user
        value = self.get_serializer(user)
        return Response(value.data)

    def list(self, request: Request, *args, **kwargs):
        user: User = request.user
        users_rows: QuerySet = service.get_users(exclude=user.username)

        users = UserSerializer(users_rows, many=True)

        return Response(users.data)

