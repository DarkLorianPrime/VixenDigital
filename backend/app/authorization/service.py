from django.contrib.auth import get_user_model
from django.db.models import Q, QuerySet


class Service:
    def __init__(self):
        self.model = get_user_model()

    def get_users(self, exclude: str) -> QuerySet:
        return self.model.objects.filter(~Q(username=exclude)).all()
