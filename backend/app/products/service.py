from typing import Dict, List

from catalogs.models import Category
from products.models import Product, Feature


class Service:
    def __init__(self):
        self.product = Product()
        self.product_dict = self.product.__class__.__dict__
        self.feature = Feature()

    def is_product_exists(self):
        self.product.objects.filter()

    def get_category(self, category: str, catalog: str, **_):
        category = Category.objects.filter(slug=category,
                                           category__slug=catalog,
                                           category__category=None)
        return category.first()

    def get_user_features(self, values: dict):
        features_list: List[Dict[str, str]] = []
        for key, element in values.items():
            if key.replace("_id", "") not in self.product_dict:
                features_list.append({key: element})

        return features_list

    def get_all_features(self, category_id: int) -> list | List[Dict[str, str | bool | int]]:
        query = self.feature.objects.filter(category=category_id)
        source = query.source_many
        if not query:
            return []

        return source

    def get_required_features(self, category_id: int) -> dict:
        query = self.feature.objects.return_("name", "values", "hits.hits._id").filter(category=category_id, required=True)
        return query.source

    def get_feature(self, category_id: int, **kwargs):
        query = self.feature.objects.filter(category=category_id, **kwargs)
        return query.source

    def delete_feature(self, feature):
        if not feature:
            return

        self.feature.objects.delete(category=feature["category"], name=feature["name"])

    def update_feature(self, feature, data):
        if not feature:
            return

        self.feature.objects.update(feature["id"], **data)
