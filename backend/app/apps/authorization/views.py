from typing import List

from django.db.models import Q
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample, inline_serializer
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from apps.authorization.models import User
from apps.authorization.serializers import RegistrationSerializer, UserSerializer, TokenSerializer
from apps.authorization.service import Service
import re

from core.permissions.permissions import IsManager

service = Service()


@extend_schema_view(
    create=extend_schema(description='Создает аккаунт по переданным параметрам',
                         operation_id="Создание аккаунта",
                         tags=["Аутентификация"]),
)
class RegistrationViewSet(ModelViewSet):
    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = RegistrationSerializer


class UsersViewSet(ModelViewSet):
    serializer_class = RegistrationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        param = self.request.query_params.get("query")
        is_staff = self.request.query_params.get("is_staff", False)
        sort = self.request.query_params.get("sort", "-id")
        fields = [field.name for field in User._meta.get_fields()]

        users = User.objects.filter(~Q(username=self.request.user.username))
        if param:
            users = users.filter(
                (Q(username__icontains=param) |
                 Q(first_name__icontains=param) |
                 Q(last_name__icontains=param)
                 ) & Q(is_staff=is_staff))

        if re.match(r"^[+-]\w+$", sort) and sort[1:] in fields:
            users = users.order_by(sort)

        return users.all()

    @extend_schema(
        operation_id="Получить информацию о аккаунте",
        description="Позволяет получать информацию о авторизованном пользователе",
        tags=["Информация о пользователях"]
    )
    def get_self(self, request: Request, *args, **kwargs) -> Response:
        user: User = request.user
        value: RegistrationSerializer = self.get_serializer(user)
        return Response(value.data)

    @extend_schema(
        operation_id="Получить список всех пользователей",
        description="Позволяет получить список пользователей, их роли и id. Запросивший в списке отсутствует.",
        responses=UserSerializer,
        tags=["Информация о пользователях"],
        parameters=[OpenApiParameter(name="query",
                                     type=str,
                                     location="query",
                                     description="Позволяет найти вхождение переданной строки в: username, "
                                                 "first_name, last_name"),
                    OpenApiParameter(name="page",
                                     location="query",
                                     type=int,
                                     description="Страница, которая будет отображена. "
                                                 "Если страница пустая - будет возвращено 404"),
                    OpenApiParameter(name="sort",
                                     location="query",
                                     type=int,
                                     examples=[OpenApiExample(name="Отсортировано по id в порядке возрастания",
                                                              value="+id"),
                                               OpenApiExample(name="Сначала сотрудники магазина",
                                                              value="-is_staff"),
                                               ],
                                     description="Параметр для сортировки. Перед параметром обязательно указывается '+' или '-'")]
    )
    def list(self, request: Request, *args, **kwargs) -> Response:
        users_rows: List[User] = self.paginate_queryset(self.get_queryset())

        users: UserSerializer = UserSerializer(users_rows, many=True)

        return self.get_paginated_response(users.data)


class ForceUserViewSet(ViewSet):
    permission_classes = [IsAdminUser]

    def set_admin(self, request: Request) -> Response:
        ...

    def update_self_admin_password(self, request: Request):
        ...

    @extend_schema(
        tags=["Информация о пользователях"],
        operation_id="Проверка правильности ввода admin code",
        description="Вход в админ-панель",
        parameters=[OpenApiParameter(name="code",
                                     examples=[OpenApiExample(name="Правильный формат кода №1", value="666-666"),
                                               OpenApiExample(name="Правильный формат кода №2", value="666666")
                                               ])],
        responses={200: inline_serializer(name="Response", fields={"access": serializers.BooleanField()})})
    def check_admin_access(self, request: Request) -> Response:
        code = request.data.get("code", "").replace("-", "")
        is_digit: bool = code.isdigit()
        is_staff: bool = request.user.is_staff

        return Response({"access": is_digit and is_staff and request.user.admin_code == int(code)})


class AccessTokenHandler(TokenObtainPairView):
    serializer_class = TokenSerializer

    @extend_schema(
        operation_id="Access аутентификация",
        tags=["Аутентификация"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class RefreshTokenHandler(TokenRefreshView):
    @extend_schema(
        operation_id="Refresh аутентификация",
        tags=["Аутентификация"]
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)