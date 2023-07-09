from django.db.models import QuerySet

from catalogs.models import Category


class Service:
    def __init__(self):
        self.model = Category

    def get_catalog(self, slug: str) -> Category:
        return self.model.objects.filter(slug=slug).first()

    def get_all_catalogs(self):
        return self.model.objects.filter(category=None)

    def get_category(self, name: str, catalog: str):
        return Category.objects.filter(slug=name, category__slug=catalog, category__category=None).first()
