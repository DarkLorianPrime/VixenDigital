from core.backend.elasticfields import KeywordField, TextField, IntegerField, DateField, BooleanField, ObjectField
from core.backend.elasticbackend import Model


class FeatureObject:
    name = KeywordField()
    value = KeywordField()
    feature_id = IntegerField()


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
    name = KeywordField()
    values = TextField()
    category = KeywordField()
    required = BooleanField()
