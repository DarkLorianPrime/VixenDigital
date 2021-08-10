from rest_framework.response import Response
from rest_framework.viewsets import ViewSet, ModelViewSet

from extras.Exceptions import APIException202
from catalogs.models import Main_Categories, Product, Features, Features_for_product
from catalogs.serializers import CategorySerializer, ProductsSerializer, FeaturesSerializer, \
    Features_for_productSerializer


class CategoriesViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    model = Main_Categories

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        if pk is None:
            returned = Main_Categories.objects.filter(category=None)
            if not returned:
                raise APIException202()
            return returned
        returned = Main_Categories.objects.filter(slug=pk).first()
        if returned is None:
            raise APIException202()
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
        returned = Main_Categories.objects.filter(category=self.get_queryset()).values('name')
        if not returned:
            return Response()
        return Response(returned)

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
        returned = self.get_serializer(data={'name': parameters.get('name'), 'category': self.get_queryset().id})
        returned.is_valid(True)
        returned.save()
        return Response([{'name': returned.validated_data['name']}])


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
        main_category = Main_Categories.objects.get(slug=globalcategory, category=None)
        give_category = Main_Categories.objects.filter(slug=category, category=main_category).first()
        products = Product.objects.filter(category=give_category)
        if give_category is None:
            return Response([])
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
        product_information = request.POST.dict()
        main_category = Main_Categories.objects.get(slug=globalcategory, category=None)
        exist_category = Main_Categories.objects.get(slug=category, category=main_category).id
        product_information['category'] = exist_category
        new_product = ProductsSerializer(data=product_information)
        new_product.is_valid(True)
        new_product.save()
        need_features = list(Features.objects.filter(category=exist_category, required=True).values_list('id', flat=True))
        for k, v in product_information.items():
            if k in exclude_list:
                continue
            if not k.isnumeric():
                new_product.instance.delete()
                return Response([{'Тип ключей FEATURES должен быть равен ID, не названию.'}])
            if int(k) in need_features:
                need_features.remove(int(k))
            data.append({'features': k, 'value': v, 'product': new_product.instance.id})
        if len(need_features) > 0:
            new_product.instance.delete()
            return Response(['Ты не указал обязательные параметры', need_features])
        d = Features_for_productSerializer(many=True, data=data)
        d.is_valid(True)
        d.save()
        return Response([{'name': new_product.validated_data["name"], 'features': data}])


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
        main_category = Main_Categories.objects.get(slug=mainCategory, category=None)
        category = Main_Categories.objects.get(slug=subCategory, category=main_category)
        all_features = Features.objects.filter(category=category)
        return Response(all_features.values('id', 'name', 'required'))

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


# unused token 13a_6gQ3ABi9GrZT59yMLw
# already created by D_Lorian
# ^V^
