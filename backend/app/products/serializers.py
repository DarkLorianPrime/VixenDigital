from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, SlugField, IntegerField, BooleanField, ListField, SerializerMethodField
from rest_framework.serializers import Serializer

from extras.slugifer import slugify
from products.models import Product, Feature

product = Product()
feature = Feature()


class ProductsSerializer(Serializer):
    name = CharField()
    description = CharField()
    slug = SlugField(required=False)
    price = IntegerField()
    count = IntegerField()
    visible = BooleanField()
    owner_id = IntegerField(source="owner")
    category_id = IntegerField(source="category")
    views = ListField(default=[])
    likes = ListField(default=[])
    features = ListField(default=[])

    def validate(self, attrs):
        print(attrs)

    def create(self, validated_data):
        validated_data['slug'] = slugify(validated_data['name'])
        return Product.objects.create(**validated_data)


class FeatureSerializer(Serializer):
    name = CharField()
    values = ListField(child=CharField())
    required = BooleanField()

    def validate(self, attrs):
        is_exists = feature.objects.filter(name=attrs["name"], category=self.context["category_id"])
        if is_exists.parse()[0]["hits"]:
            raise ValidationError(code=409, detail={"feature": "already exists"})

        return attrs

    def create(self, validated_data):
        validated_data["category"] = self.context["category_id"]

        feature(**validated_data)
        return validated_data
