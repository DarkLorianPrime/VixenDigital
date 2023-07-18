from core.backend.elasticfields import KeywordField, TextField, IntegerField, DateField, BooleanField, ObjectField
from core.backend.elasticbackend import Model
import django.db.models as django_models

ORDER_CHOICES = [
    ("CREATED", "Создано"),
    ("SENT", "Отправлено"),
    ("WAIT_RECEIVE", "Доступно для получения"),
    ("RECEIVED", "Получено"),
    ("CANCELLED", "Отменен")
]


class FeatureObject:
    display_name = KeywordField()
    values = KeywordField()
    slug = KeywordField()
    unit = TextField(null=True)


class Cities(Model):
    name = KeywordField()


class CountObject:
    count = IntegerField()
    city = TextField()


class ReviewObject:
    rating = IntegerField()
    text = TextField(null=True)
    disadvantages = TextField(null=True)
    advantages = TextField(null=True)
    images = TextField()
    likes = IntegerField()
    dislikes = IntegerField()
    real_buyer = BooleanField()
    created_at = DateField()
    updated_at = DateField()


class Product(Model):
    name = KeywordField()
    description = TextField()
    category = IntegerField()
    slug = KeywordField()
    price = IntegerField()
    count = ObjectField(CountObject)
    created = DateField()
    updated = DateField()
    discount = IntegerField()
    logos = TextField()
    visible = BooleanField()
    owner = IntegerField()  # ORGANIZATION
    views = IntegerField(null=True)
    likes = IntegerField(null=True)
    reviews = ObjectField(ReviewObject)
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


class CartItem(django_models.Model):
    count = django_models.IntegerField()
    slug = django_models.SlugField()


class FavouriteItem(django_models.Model):
    slug = django_models.SlugField()


class DeliveryInformation(django_models.Model):
    address = django_models.CharField()
    floor = django_models.IntegerField()
    date = django_models.DateTimeField()
    is_list_exists = django_models.BooleanField()
    is_house = django_models.BooleanField()


class Order(django_models.Model):
    status = django_models.CharField(choices=ORDER_CHOICES)
    is_delivery = django_models.BooleanField()
    address = django_models.ForeignKey(DeliveryInformation, on_delete=django_models.CASCADE, related_name="Order_delivery")
