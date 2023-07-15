from rest_framework.exceptions import ValidationError
from rest_framework.fields import CharField, SlugField, IntegerField, BooleanField, ListField
from rest_framework.serializers import Serializer

from extras.slugifer import slugify
from products.models import Product, Feature
from products.service import Service

product = Product()
feature = Feature()
service = Service()


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
    display_name = CharField()
    name = SlugField(default=None)
    values = ListField(child=CharField())
    category = CharField(default=None)
    many = BooleanField(default=None)
    required = BooleanField()

    @property
    def method(self):
        return self.context["request"].method

    def validate_category(self, _):
        return self.context["category_id"]

    def validate_display_name(self, name):
        self.context["name"] = name

        if not self.instance:
            source = feature.objects.filter(display_name=name, category=self.context["category_id"]).source
        else:
            source = self.instance

        if self.method != "POST" and source["name"] == self.instance["name"]:
            return name

        if source:
            raise ValidationError(code=409, detail="already exists")

        return name

    def validate_name(self, _=None):
        name = self.context["name"]

        if not name:
            raise ValidationError(detail="\"display\" cannot be empty")

        return slugify(name)

    def create(self, validated_data):
        feature(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        if validated_data.get("display_name"):
            validated_data["name"] = self.validate_name()

        service.update_feature(instance, validated_data)
        instance.update(validated_data)
        return instance
