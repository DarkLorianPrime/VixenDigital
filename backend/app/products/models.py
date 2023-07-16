from core.backend.elasticfields import KeywordField, TextField, IntegerField, DateField, BooleanField, ObjectField
from core.backend.elasticbackend import Model


class FeatureObject:
    display_name = KeywordField()
    values = KeywordField()
    slug = KeywordField()
    unit = TextField(null=True)


class Product(Model):
    name = KeywordField()
    description = TextField()
    category = IntegerField()
    slug = KeywordField()
    price = IntegerField()
    count = IntegerField()
    created = DateField()
    updated = DateField()
    visible = BooleanField()
    owner = IntegerField()  # ORGANIZATION
    views = IntegerField(null=True)
    likes = IntegerField(null=True)
    article = KeywordField()
    features = ObjectField(FeatureObject)


class Feature(Model):
    display_name = KeywordField()
    name = KeywordField()
    values = TextField()
    category = KeywordField()
    many = BooleanField()
    required = BooleanField()
    unit = TextField(null=True)
