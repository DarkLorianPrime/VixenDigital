from django.db import models


class Main_Categories(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    category = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.name


class Access_Token(models.Model):
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token


class Features(models.Model):
    category = models.ForeignKey(Main_Categories, on_delete=models.CASCADE, related_name='Catalog_Features')
    name = models.CharField(max_length=200)
    required = models.BooleanField()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Main_Categories, on_delete=models.CASCADE, related_name='product_category')
    description = models.TextField()
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    price = models.IntegerField()
    stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.slug}'


class Features_for_product(models.Model):
    features = models.ForeignKey(Features, on_delete=models.CASCADE, related_name='featuress')
    value = models.CharField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return f'{self.features.name} - {self.value}'
