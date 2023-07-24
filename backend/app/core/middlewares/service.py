from apps.catalogs.models import Category


class Service:
    def get_category(self, catalog: str, name: str) -> Category | None:
        return Category.objects.filter(slug=name, category__slug=catalog, category__category=None).first()

    def get_catalog(self, slug: str, _: str) -> Category | None:
        return Category.objects.filter(slug=slug).first()
