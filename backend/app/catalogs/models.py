from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, blank=True)
    category = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL, related_name="categories")

    def __str__(self):
        return self.name

# // temporarily deprecated
# class AccessToken(models.Model):
#     token = models.CharField(max_length=255)
#
#     def __str__(self):
#         return self.token


class Features(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='Features_Category')
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=2000)
    required = models.BooleanField()

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='Product_Category')
    description = models.TextField()
    name = models.CharField(max_length=100)
    slug = models.SlugField()
    price = models.IntegerField()
    stock = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    features = models.JSONField("Features_Product", default=dict)

    def __str__(self):
        return f'{self.name} - {self.slug}'


# class FeaturesForProduct(models.Model):
#     category = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='FFP_Category')
#     features = models.ForeignKey('Features', on_delete=models.CASCADE, related_name='FeaturesFeatures_Features')
#     value = models.CharField(max_length=500)
#     product = models.ForeignKey('Product', on_delete=models.CASCADE, related_name='FeaturesProduct_Features')
#
#     def __str__(self):
#         return f'{self.features.name} - {self.value} - {self.product.name}'
