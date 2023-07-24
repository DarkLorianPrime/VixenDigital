from django.db.models import QuerySet, Q
from rest_framework.exceptions import ValidationError

from apps.authorization.models import User
from apps.catalogs.models import Category, Organization


class CategoryRepository:
    def __init__(self):
        self.model = Category

    def get_catalog(self, slug: str, _: str) -> Category:
        return self.model.objects.filter(slug=slug).first()

    def get_all_catalogs(self):
        return self.model.objects.filter(category=None)

    def get_category(self, catalog: str, name: str):
        return self.model.objects.filter(slug=name, category__slug=catalog, category__category=None).first()

    def is_category_exists(self, category: str, catalog: str = None):
        return self.model.objects.filter(name=category, category=catalog).exists()

    def create_category(self, **validated_data) -> None:
        return self.model.objects.create(**validated_data)

    def is_exist_category(self, category: str, catalog: str = None) -> bool:
        if self.is_category_exists(category, catalog):
            raise ValidationError('already exists', code=409)

        return False


class OrganizationRepository:
    def __init__(self):
        self.model = Organization

    def is_organization_exists(self, organization_name: str):
        return self.model.objects.filter(name=organization_name).exists()

    def get_maintainer(self, user: User) -> User:
        return self.model.objects.filter(Q(maintainer=user) | Q(contributors=user)).first().maintainer

    def organization_logo_delete(self, instance: Organization) -> None:
        instance.logo.delete()

    def get_contributors(self, contributors_list: list) -> QuerySet:
        return User.objects.filter(id__in=contributors_list).all()

    def is_exist_organization(self, name: str) -> str:
        if self.is_organization_exists(name):
            raise ValidationError('already exists', code=409)

        return name

    def get_organization(self, *args, **kwargs) -> Organization:
        return self.model.objects.filter(*args, **kwargs).first()
