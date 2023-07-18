from django.contrib.auth.models import AbstractUser
from django.db import models
from django_minio_backend import MinioBackend


class Notifications(models.Model):
    text = models.TextField()
    name = models.CharField()
    picture = models.ImageField(storage=MinioBackend(bucket_name="private-bucket"), null=True, blank=True)
    url_to = models.URLField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    send_date = models.DateTimeField(auto_now_add=True)
    read_date = models.DateTimeField(null=True, default=None)


class User(AbstractUser):
    middle_name = models.CharField(max_length=48)
    notifications = models.ManyToManyField("Notifications")
    cart = models.ManyToManyField("products.CartItem")
    favourite = models.ManyToManyField("products.FavouriteItem")
    logo = models.ImageField(storage=MinioBackend(bucket_name="private-bucket"), blank=True, null=True)
