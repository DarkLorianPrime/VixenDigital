from django.db import connection
from django.db.models import Value
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from catalogs.models import Categories, Product, Features, FeaturesForProduct
from catalogs.serializers import CategorySerializer, ProductsSerializer, FeaturesSerializer, \
    Features_for_productSerializer


class CategoriesViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    model = Categories

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            returned = Categories.objects.filter(category=None)
            return returned
        returned = Categories.objects.filter(slug=pk).first()
        return returned

    def retrieve(self, request, *args, **kwargs):
        """
        Description:
        For a construction of the type: URL/catalog/
        For example: darklorian.space/Computers/
        ------
        Request action: GET
        ------
        :return: Will returned all categories located in specified catalog
        """
        returned = Categories.objects.filter(category=self.get_queryset()).values('name', 'slug')
        returned_data = returned if self.get_queryset() is not None else [{'Catalog not found'}]
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
        parameters = request.POST.dict()
        returned = self.get_serializer(data={**parameters, 'category': self.get_queryset().id})
        returned.is_valid(True)
        returned.save()
        return Response([{returned.validated_data['name']}])


class Products(ViewSet):
    def list(self, request, globalcategory, category):
        """
        Description:
        For a construction of the type: URL/catalog/category
        For example: darklorian.space/Computers/Processors
        Get all products specified in specified category
        ------
        Request action: GET
        ------
        :param:  globalcategory : slug:
            catalog in which there may be a category ↓
        :param: category : slug:
            category, in which we are looking for a product
        :return: List of products
        """
        main_category = Categories.objects.get(slug=globalcategory, category=None)
        give_category = Categories.objects.filter(slug=category, category=main_category).first()
        products = Product.objects.filter(category=give_category)
        if give_category is None:
            return Response([{f'Категория {category} не найдена.'}])
        if products.count() <= 0:
            return Response([{f'Продукция {give_category} не найдена.'}])
        return Response([{products.values()}])

    def create(self, request, globalcategory, category):
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
        data = []
        fucking_json = {}
        product_information = request.POST.dict()
        catalog = Categories.objects.get(slug=globalcategory, category=None)
        category = Categories.objects.get(slug=category, category=catalog).id
        product_information['category'] = category
        new_product = ProductsSerializer(data=product_information)
        new_product.is_valid(True)
        new_product.save()
        required_features = list(
            Features.objects.filter(category=category, required=True).values_list('slug', flat=True))
        for features_name, value_name in product_information.items():
            if features_name in exclude_list:
                continue
            # if not features_name.isnumeric():
            #     new_product.instance.delete()
            #     return Response([{'Тип ключей FEATURES должен быть равен ID, а не названию.'}])
            if features_name in required_features:
                required_features.remove(features_name)
            fucking_json[features_name] = value_name
        if len(required_features) > 0:
            new_product.instance.delete()
            return Response(['Ты не указал обязательные features (slug):', required_features])
        print(fucking_json)
        new_product.instance.features = fucking_json
        new_product.instance.save()
        # serialized = Features_for_productSerializer(many=True, data=data)
        # serialized.is_valid(True)
        # serialized.save()
        return Response([{'name': new_product.validated_data["name"], 'features': fucking_json}])


class FeaturesViewSet(ViewSet):
    def list(self, request, mainCategory, subCategory):
        """
        Description:
        For a construction of the type: URL/catalog/category/features/
        For example: darklorian.space/Computers/Processors/features/
        Get all features specified in specified products
        ------
        Request action: GET
        ------
        :param:  globalcategory : slug:
            catalog in which there may be a category ↓
        :param: category : slug:
            category, in which we are looking for a product
        :return: List of features of the specified products
        """
        main_category = Categories.objects.get(slug=mainCategory, category=None)
        category = Categories.objects.filter(slug=subCategory, category=main_category).first()
        all_features = Features.objects.filter(category=category)
        return Response(all_features.values('id', 'name', 'slug', 'required'))

    def create(self, request, mainCategory, subCategory):
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
        request_data['category'] = subCategory
        request_data['catalog'] = mainCategory
        serialized = FeaturesSerializer(data=request_data)
        serialized.is_valid(True)
        serialized.save()
        return Response({"name": [serialized.validated_data['name']], "id": serialized.instance.id})


class SearchViewset(ViewSet):
    def get(self, request, mainCategory, subCategory):
        # query = '''SELECT product_id FROM catalogs_FeaturesForProduct WHERE features_id = %s and value = %s and catalogs_featuresforproduct.category_id = %s \n'''
        # query_add = '''INTERSECT SELECT product_id FROM catalogs_FeaturesForProduct WHERE features_id = %s and value=%s and catalogs_featuresforproduct.category_id = %s'''
        get_data = self.request.GET
        catalog = Categories.objects.filter(slug=mainCategory, category=None)
        category = Categories.objects.filter(slug=subCategory, category=catalog.first())
        if not category.exists():
            return Response(['Category not found'])
        category = category.first()
        query_args = {}
        for features_name, features_value in get_data:
            query_args[str(features_name)] = str(features_value)
        # for features_name, features_value in get_data.items():
        #     products.append(str(features_name))
        #     products.append(str(features_value))
        #     products.append(str(category.first().id))
        # final_query = query if len(get_data.keys()) <= 1 else query + query_add * (len(get_data.keys()) - 1)
        finally_get = Product.objects.filter(features__contains=query_args, category=category.first()).values('name', 'slug')
        # with connection.cursor() as cursor:
        #     try:
        #         cursor.execute(final_query, products)
        #         row = cursor.fetchall()
        #         lister = [element[0] for element in row]
        #         products = Product.objects.filter(id__in=lister).values('name')
        #     except:
        #         products = ['Not found']
        return Response(finally_get)

# unused token 13a_6gQ3ABi9GrZT59yMLw
# already created by D_Lorian //
# ^V^
