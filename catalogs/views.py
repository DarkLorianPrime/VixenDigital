import json

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from catalogs.models import Product, Features, Token
from catalogs.models import Class as Category
from catalogs.serializers import CategorySerializer, ProductsSerializer, FeaturesSerializer


class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    model = Category

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            returned = Category.objects.filter(category=None)
            return returned
        returned = Category.objects.filter(slug=pk).first()
        return returned

    def retrieve(self, request, *args, **kwargs):
        """
        Description:
        For a construction of the type: URL/catalog/
        For example: darklorian.space/Computers/
        ------
        Request action: GET
        ------
        :return: Will returned all Category located in specified catalog
        """
        returned = Category.objects.filter(category=self.get_queryset()).values('id', 'name', 'category__name', 'slug')
        returned_data = returned if self.get_queryset() is not None else {'error': 'catalog not found'}
        print(returned_data)
        return Response(returned_data)

    def post(self, request, *args, **kwargs):
        """
        Description:
        Creating a new section in the catalog section
        ------
        Request Action: POST
        ------
        Raises:
        :raise An exception will be thrown if one of the parameters was not passed
        :raise If this category already exists
        -----
        POST data (Parameters):
        :param: name : str
            Name of creating section
        :param: category : slug
            An unspecified parameter. Taken from queryset
        :return:
            Response with name of created category
        """
        if not request.access:
            return Response({'error': 'Token expired', 'token': Token.objects.first().token})
        parameters = request.POST.dict()
        returned = self.get_serializer(data={**parameters, 'category': self.get_queryset().id})
        returned.is_valid(raise_exception=True)
        returned.save()
        return Response({'name': returned.validated_data['name']})

    def destroy(self, request, *args, **kwargs):
        self.model.objects.filter(pk=json.loads(request.body)['id']).delete()
        return Response({'status': 'ok'})


class Products(ViewSet):
    def list(self, request, catalog, category):
        """
        Description:
        For a construction of the type: URL/catalog/category
        For example: darklorian.space/Computers/Processors
        Get all products specified in specified category
        ------
        Request action: GET
        ------
        :param:  catalog : slug:
            catalog in which there may be a category ↓
        :param: category : slug:
            category, in which we are looking for a product
        :return: List of products
        """
        catalog = Category.objects.filter(slug=catalog, category=None).first()
        category = Category.objects.filter(slug=category, category=catalog).first()
        products = Product.objects.filter(category=category)
        if category is None:
            return Response({'error': f'Категория {category} не найдена.'})
        if products.count() <= 0:
            return Response({'error': f'Продукция {category} не найдена.'})
        return Response(products.values())

    def create(self, request, catalog, category):
        """
        Description:
        Creates a new product in this category
        ------
        Request Action: POST
        ------
        Raises:
        :raise An exception will be thrown if one of the parameters was not passed
        -----
        POST data (Parameters):
        :param: name : str
            Name of creating product.
        :param: category : model.id
            An unspecified parameter.
        :param: (Many) features : many args
            Features from the features list.
        :param: description : str
            Information about this product
        :param: slug : slug
            An unspecified parameter.
        :param: price : int
            Price in rubles
        :param: stock : int
            quantity of goods in stock
        :return:
            Response with name of created product
        """
        exclude_list = ['name', 'description', 'price', 'stock', 'category']
        product_information = request.POST.dict()
        catalog = Category.objects.filter(slug=catalog, category=None).first()
        category = Category.objects.filter(slug=category, category=catalog)
        if not category.exists():
            return Response({'error': 'Category not found'})
        product_information['category'] = category.first().id
        new_product = ProductsSerializer(data=product_information)
        new_product.is_valid(raise_exception=True)
        required_features = Features.objects.filter(category=category.first(), required=True).values_list('slug',
                                                                                                          flat=True)
        features_json = {features_name: value_name for features_name, value_name in product_information.items() if features_name not in exclude_list}
        required = {features_name: value_name for features_name, value_name in features_json.items() if
                    features_name in required_features}
        not_insered_required = set(required_features) - set(required)
        if not_insered_required:
            return Response({'error': 'Ты не указал обязательные features (slug):', 'arguments': not_insered_required})
        new_product.features = features_json
        new_product.save()
        return Response([{'name': new_product.validated_data["name"], 'features': features_json}])


class FeaturesViewSet(ViewSet):
    def list(self, request, catalog, category):
        """
        Description:
        For a construction of the type: URL/catalog/category/features/
        For example: darklorian.space/Computers/Processors/features/
        Get all features specified in specified products
        ------
        Request action: GET
        ------
        :param:  catalog : slug:
            catalog in which there may be a category ↓
        :param: category : slug:
            category, in which we are looking for a product
        :return: List of features of the specified products
        """
        main_category = Category.objects.filter(slug=catalog, category=None)
        category = Category.objects.filter(slug=category, category=main_category.first())
        if not category.exists():
            return Response({'error': 'Category not found'})
        category = category.first()
        all_features = Features.objects.filter(category=category)
        return Response(all_features.values('id', 'name', 'slug', 'required'))

    def create(self, request, catalog, category):
        """
        Description:
        Creates a new product in this category
        ------
        Request Action: POST
        ------
        Raises:
        :raise An exception will be thrown if one of the parameters was not passed
        -----
        POST data (Parameters):
        :param: name : str
            Name of creating product.
        :param: required : bool
        :return:
            Response with name of created feature
        """
        request_data = request.POST.dict()
        request_data['category'] = category
        request_data['catalog'] = catalog
        serialized = FeaturesSerializer(data=request_data)
        serialized.is_valid(raise_exception=True)
        serialized.save()
        return Response({"name": [serialized.validated_data['name']], "id": serialized.instance.id})


class SearchViewset(ViewSet):
    def get(self, request, catalog, category):
        get_data = self.request.GET
        catalog = Category.objects.filter(slug=catalog, category=None)
        category = Category.objects.filter(slug=category, category=catalog.first())
        if not category.exists():
            return Response({'error': 'Category not found'})
        category = category.first()
        finally_get = Product.objects.filter(features__contains=get_data, category=category)
        return Response(finally_get.values('name', 'slug'))


"""
Older Search:
query = '''SELECT product_id FROM catalogs_FeaturesForProduct WHERE features_id = %s and value = %s and catalogs_featuresforproduct.category_id = %s \n'''
query_add = '''INTERSECT SELECT product_id FROM catalogs_FeaturesForProduct WHERE features_id = %s and value=%s and catalogs_featuresforproduct.category_id = %s'''
final_query = query if len(get_data.keys()) <= 1 else query + query_add * (len(get_data.keys()) - 1)
with connection.cursor() as cursor:
    try:
        cursor.execute(final_query, products)
        row = cursor.fetchall()
        lister = [element[0] for element in row]
        products = Product.objects.filter(id__in=lister).values('name')
    except:
        products = ['Not found']
I dont now what is the search:
for features_name, features_value in get_data.items():
    products.append(str(features_name))
        products.append(str(features_value))
            products.append(str(category.first().id))
"""
# unused token 13a_6gQ3ABi9GrZT59yMLw
# already created by D_Lorian //


# Wait, its a shit code
# Always has been.
