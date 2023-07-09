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

    def get_category(self, category: str, catalog: str):
        print(category, catalog)
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

    def get_all_features(self, category_id: int) -> dict:
        query = self.feature.objects.return_("name", "values", "required").filter(category=category_id)
        query.parse()
        return query.source_

    def get_required_features(self, category_id: int) -> dict:
        return self.feature.objects.filter(category=category_id, required=True)[0]["hits"]

