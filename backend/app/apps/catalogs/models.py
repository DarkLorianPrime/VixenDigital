from django.db import models
from django_minio_backend import MinioBackend


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    category = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name="categories")
    logo = models.ImageField(storage=MinioBackend(bucket_name="private-bucket"), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
