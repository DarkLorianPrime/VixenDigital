from django.db import models
from django_minio_backend import MinioBackend


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    category = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name="categories")

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Organization(models.Model):
    name = models.CharField(max_length=128, unique=True)
    maintainer = models.ForeignKey("authorization.User", null=True, on_delete=models.SET_NULL, related_name="maintainer")
    contributors = models.ManyToManyField("authorization.User", blank=True)
    verified = models.BooleanField(default=False)
    description = models.TextField()
    slug = models.SlugField(blank=True, unique=True)
    logo = models.ImageField(storage=MinioBackend(bucket_name="private-bucket"))

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

