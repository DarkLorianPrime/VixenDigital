from core.backend.elasticfields import KeywordField, TextField, IntegerField, DateField, BooleanField, ObjectField
from core.backend.elasticbackend import Model


class FeatureObject:
    display_name = KeywordField()
    values = KeywordField()
    slug = KeywordField()


class Product(Model):
    name = TextField()
    description = TextField()
    category = IntegerField()
    slug = TextField()
    price = IntegerField()
    count = IntegerField()
    created = DateField()
    updated = DateField()
    visible = BooleanField()
    owner = IntegerField()
    views = IntegerField()
    likes = IntegerField()
    features = ObjectField(FeatureObject)


class Feature(Model):
    display_name = KeywordField()
    name = KeywordField()
    values = TextField()
    category = KeywordField()
    many = BooleanField()
    required = BooleanField()
