from rest_framework.exceptions import ValidationError

from apps.catalogs.models import Category


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
