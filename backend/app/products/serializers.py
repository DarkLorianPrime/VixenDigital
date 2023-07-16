import datetime
import random

from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, SlugField, IntegerField, BooleanField, ListField
from rest_framework.serializers import Serializer

from catalogs.repositories import OrganizationRepository
from extras.slugifer import slugify
from products.models import Feature
from products.repositories import ProductRepository, FeatureRepository

products_repo = ProductRepository()
features_repo = FeatureRepository()
organization_repo = OrganizationRepository()


def random_value():
    length = 24
    return "".join([str(random.randint(0, 9)) for _ in range(length)])


class SmallInfoProductSerializer(Serializer):
    name = CharField()
    description = CharField()
    slug = SlugField()
    visible = BooleanField()
    article = IntegerField()
    views = ListField()
    likes = ListField()
    owner = SlugField()


class FullInfoProductSerializer(Serializer):
    name = CharField()
    description = CharField()
    slug = SlugField(default=False)
    price = IntegerField(min_value=1)
    count = IntegerField(min_value=0)
    visible = BooleanField(default=False)
    owner = SlugField()
    category = IntegerField(default=None)
    views = ListField(default=[])
    likes = ListField(default=[])
    features = ListField(default=None)
    article = IntegerField(default=None)

    def validate_category(self, _):
        return self.context["category_id"]

    def validate_name(self, name):
        self.context["name"] = name
        if products_repo.is_product_exists(name, self.context["category_id"]):
            raise ValidationError("already exists")

        return name

    def validate_owner(self, owner_slug):
        organization = organization_repo.get_organization(slug=owner_slug)
        if not organization:
            raise ValidationError("organization not found")

        if not organization.verified:
            raise ValidationError("organization is not verified")

        return organization.id

    def validate_slug(self, _):
        return slugify(self.context["name"])

    def create(self, validated_data: dict):
        date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        validated_data["created"] = date
        validated_data["updated"] = date
        validated_data["article"] = random_value()
        products_repo.create_product(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        validated_data["updated"] = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
        products_repo.update_product(instance, validated_data)
        instance.update(validated_data)
        return instance


class FeatureSerializer(Serializer):
    display_name = CharField()
    unit = CharField(allow_blank=True)
    name = SlugField(default=None)
    values = ListField(child=CharField(), required=True)
    category = CharField(default=None)
    many = BooleanField(default=None)
    required = BooleanField()

    @property
    def method(self):
        return self.context["request"].method

    def validate_category(self, _):
        return self.context["category_id"]

    def validate_display_name(self, name: str) -> str:
        self.context["name"] = name
        instance: Feature | dict = self.instance or {}
        instance_name = instance.get("display_name", None)

        if instance_name == name:
            return name

        if instance_name is None:
            if features_repo.is_feature_exists(display_name=name, category_id=self.context["category_id"]):
                raise ValidationError(code=409, detail="already exists")

        return name

    def validate_name(self, _=None) -> str:
        name = self.context["name"]

        if not name:
            raise ValidationError(detail="\"display\" cannot be empty")

        return slugify(name)

    def create(self, validated_data: dict) -> dict:
        if validated_data.get("values"):
            validated_data["values"] = list(map(lambda value: value.lower(), validated_data["values"]))

        features_repo.create_feature(**validated_data)
        return validated_data

    def update(self, instance: dict, validated_data: dict) -> dict:
        if validated_data.get("display_name"):
            validated_data["name"] = self.validate_name()

        if validated_data.get("values"):
            validated_data["values"] = list(map(lambda value: value.lower(), validated_data["values"]))

        features_repo.update_feature(instance, validated_data)
        instance.update(validated_data)
        return instance
