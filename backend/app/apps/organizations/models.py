#  Copyright (c) 2023. Kasimov Alexander, Ulyanovsk. All right reserved.

from django.db import models
from django_minio_backend import MinioBackend


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
