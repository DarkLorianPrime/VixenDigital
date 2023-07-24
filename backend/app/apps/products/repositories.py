from typing import Dict, List, Any, KeysView, Set, Tuple

from apps.products.models import Product, Feature


class FeatureRepository:
    def __init__(self) -> None:
        self.model = Feature()
        self.product_dict: dict = Product().__class__.__dict__

    def get_user_features(self, values: dict) -> list:
        features_list: List[Dict[str, str]] = []
        for key, element in values.items():
            if key.replace("_id", "") not in self.product_dict:
                features_list.append({key: element})

        return features_list

    def get_all_features(self, category_id: int) -> list | List[Dict[str, str | bool | int]]:
        query = self.model.objects.filter(category=category_id)
        source = query.source_many
        if not query:
            return []

        return source

    def get_required_features(self, category_id: int) -> list:
        return_list = ["name", "values", "required", "many", "unit", "display_name"]
        query = self.model.objects.return_(*return_list).filter(category=category_id)
        return query.source

    def get_feature(self, category_id: int, **kwargs) -> dict:
        query = self.model.objects.filter(category=category_id, **kwargs)
        return query.source

    def delete_feature(self, feature: dict) -> None:
        if not feature:
            return

        self.model.objects.delete(category=feature["category"], name=feature["name"])

    def update_feature(self, feature: dict, data: dict) -> None:
        if not feature:
            return

        self.model.objects.update(feature["id"], **data)

    def is_feature_exists(self, display_name: str, category_id: str) -> dict:
        return self.model.objects.filter(display_name=display_name, category=category_id).source

    def create_feature(self, **data):
        self.model(**data)

    def difference_features(self, first_list: Set[Any], second_list: KeysView) -> Tuple[Dict[str, List[str]], Set[str]]:
        difference = set(first_list) - set(second_list)
        union = set(first_list) & set(second_list)
        troubles = {element: ["This feature is required"] for element in difference}

        return troubles, union

    def check_value_valid(self, true_fields: Dict[str, Any], validated_fields: Dict[str, Any]) -> Dict[str, List]:
        not_valid_fields = {}
        for key, values in true_fields.items():
            validated_values = validated_fields.get(key)
            if validated_values is None:
                continue

            if validated_fields.get(key) not in values["values"]:
                not_valid_fields[key] = ["This feature value is not valid"]

        return not_valid_fields


class ProductRepository:
    def __init__(self):
        self.model = Product()

    def is_product_exists(self, product_name, category_id):
        query = self.model.objects.filter(name=product_name, category=category_id)
        return query.source

    def get_all_products(self, category_id: str, visible: bool = None):
        query_params = {"category": category_id}
        if visible is not None:
            query_params["visible"] = visible

        query = self.model.objects.filter(**query_params)
        return query.source_many

    def create_product(self, **validated_data):
        return self.model(**validated_data)

    def get_product(self, category_id: int, **kwargs) -> dict:
        query = self.model.objects.filter(category=category_id, **kwargs)
        return query.source

    def delete_product(self, product: dict) -> None:
        if not product:
            return

        self.model.objects.delete(category=product["category"], slug=product["slug"])

    def update_product(self, product: dict, data: dict) -> None:
        if not product:
            return

        self.model.objects.update(product["id"], **data)