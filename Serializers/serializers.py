from rest_framework import serializers
from rest_framework.serializers import Serializer, ModelSerializer
from transliterate import translit

from catalogs.models import Main_Categories, Product, Features
from Serializers.Exceptions import APIException202


def is_exist_category(value):
    if Main_Categories.objects.filter(name=value).exists():
        raise APIException202({'errors': 'already exists'})


def is_exist_subcategory(value):
    if Main_Categories.objects.filter(name=value['name'], category__name=value['category']).exists():
        raise APIException202({'errors': 'already exists'})


def validator_main(value):
    if not Main_Categories.objects.filter(main_categories=None).exists():
        raise APIException202({'errors': 'anything not found'})


def validator_sub(value):
    if not Main_Categories.objects.filter(main_categories=not None).exists():
        raise APIException202({'errors': 'anything not found'})


class Category_Serializer(Serializer):
    name = serializers.CharField(validators=[is_exist_category])

    def create(self, validated_data):
        validated_data['slug'] = translit(validated_data['name'], 'ru', reversed=True).replace("'", '').replace(" ",
                                                                                                                '_').lower()
        return Main_Categories.objects.create(**validated_data)


class Sub_Category_Serializer(Serializer):
    name = serializers.CharField()
    category = serializers.SlugField()

    def create(self, validated_data):
        validated_data['category'] = Main_Categories.objects.filter(slug=validated_data['category']).first()
        validated_data['slug'] = translit(validated_data['name'], 'ru', reversed=True).replace("'", '').replace(" ",
                                                                                                                '_').lower()
        is_exist_subcategory(validated_data)
        return Main_Categories.objects.create(**validated_data)


class Get_Category_Serializer(Serializer):
    object = serializers.ListField(validators=[validator_main], )
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        return validated_data


class Get_SubCategory_Serializer(Serializer):
    object = serializers.ListField(validators=[])
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        return validated_data


class Get_Products_Serializer(Serializer):
    object = serializers.ListField()
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        return validated_data


class Products_Serializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class Get_Features_Serializer(Serializer):
    object = serializers.ListField()
    count = serializers.IntegerField()

    def return_serialize(self, validated_data):
        return validated_data


class Features_Serializer(Serializer):
    name = serializers.CharField()
    category = serializers.SlugField()

    def create(self, validated_data):
        data = Main_Categories.objects.filter(slug=validated_data['category']).first()
        validated_data['category'] = data
        return Features.objects.create(**validated_data)

# class Products_Serializer(Serializer):
#    category = serializers.CharField()
#    feauters = serializers.ListField()
#    description = serializers.CharField()
#    name = serializers.CharField()
#    slug = serializers.CharField()
#    price = serializers.IntegerField()
