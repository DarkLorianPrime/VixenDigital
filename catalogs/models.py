from django.db import models


class Main_Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Sub_Categories(models.Model):
    name = models.CharField(max_length=100);
    main_category = models.ForeignKey(Main_Categories, on_delete=models.CASCADE, related_name='whose_category')
    slug = models.SlugField(max_length=100)

    def __str__(self):
        return self.name


class Access_Token(models.Model):
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token


class Features_gyroscooter(models.Model):
    name = models.CharField(max_length=100)


class DiagonalWheel_gyroscooter(models.Model):
    diagonal = models.FloatField(max_length=100)


class Product_gyroscooter(models.Model):
    sub_category = models.ForeignKey(Sub_Categories, on_delete=models.CASCADE, related_name='product_category')
    features = models.ManyToManyField(Features_gyroscooter)
    diagonal_wheel = models.ForeignKey(DiagonalWheel_gyroscooter, on_delete=models.CASCADE, related_name='diagonal_wheel')