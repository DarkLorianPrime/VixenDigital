from rest_framework.response import Response
from rest_framework.views import APIView
from transliterate import translit
from catalogs.models import Main_Categories, Access_Token, Sub_Categories

errors = [{'code': '0', 'error': 'already exists'}, {'code': '3', 'error': 'token not found'}]


class Start_Page(APIView):
    def get(self, request):
        returned_all_categories = []
        if not Main_Categories.objects.exists():
            return Response({'response': {'code': '4', 'error': 'anything not found'}}, status=400)
        for one_category in Main_Categories.objects.all():
            returned_all_categories.append(f'{one_category.name} - {request.META["HTTP_HOST"]}/{one_category.slug}')
        return Response({"response": {'code': '2', 'object': returned_all_categories}}, status=200)

    def post(self, request):
        token, new_category = request.GET['access_token'], request.GET['name'].capitalize()
        if not Access_Token.objects.filter(token=token).exists():
            return Response({'response': errors[1]}, status=400)
        if Main_Categories.objects.filter(name=new_category).exists():
            return Response({'response': errors[0]}, status=400)
        slug_rep = translit(new_category, 'ru', reversed=True).replace("'", '').replace(" ", '_')
        Main_Categories.objects.create(name=new_category, slug=slug_rep)
        return Response({'response': {'code': '1', 'object': f'{new_category}'}}, status=200)


class Codes(APIView):
    code_list = [{'description': 'Возвращает сообщение о том, что объект уже зарегистрирован в базе', 'code': '0'},
                 {'description': 'Возвращает сообщение о том, что операция прошла успешно. POST методы',
                  'code': '1'},
                 {'description': 'Возвращает сообщение о том, что операция прошла успешно. GET методы',
                  'code': '2'},
                 {'description': 'Возвращает сообщение о том, что токен неверный', 'code': '3'},
                 {'description': 'Возвращает сообщение о том, что объектов в базе нет', 'code': '4'},
                 {'description': 'Возвращает сообщение о том, что данного объекта в базе нет', 'code': '5'}]

    def get(self, request):
        return Response({'response': self.code_list, 'code': '2'}, status=200)

    def post(self, request):
        return Response({'response': self.code_list, 'code': '2'}, status=200)


class Sub_Category(APIView):
    def get(self, request, mainCategory):
        All_sub_categories = []
        all_categories = Sub_Categories.objects.filter(
            main_category=Main_Categories.objects.filter(slug=mainCategory).first())
        if not all_categories.exists():
            return Response({'response': {'code': '4', 'error': f'Subcategories not found'}},
                            status=400)
        for one_of_sub_category in all_categories:
            All_sub_categories.append(f'{one_of_sub_category.name} - {request.META["HTTP_HOST"]}/{one_of_sub_category.slug}')
        return Response({'response': {'code': '2', 'objects': All_sub_categories}})

    def post(self, request, mainCategory):
        token, new_category = request.GET['access_token'], request.GET['name'].capitalize()
        if not Access_Token.objects.filter(token=token).exists():
            return Response({'response': errors[1]}, status=400)
        main_category_model = Main_Categories.objects.filter(slug=mainCategory).first()
        all_categories = Sub_Categories.objects.filter(main_category=main_category_model)
        if all_categories.exists():
            return Response({'response': errors[0]}, status=400)
        slug_rep = translit(new_category, 'ru', reversed=True).replace("'", '').replace(" ", '_')
        Sub_Categories.objects.create(name=new_category, main_category=main_category_model, slug=slug_rep)
        return Response({'response': {'code': '1', 'object': new_category}}, status=200)


class Products(APIView):
    def get(self, request, mainCategory, subCategory):
        products = []
        product_in_subcategory = Sub_Categories.objects.filter(name=subCategory,
                                                               main_category=Main_Categories.objects.filter(
                                                                   name=mainCategory).first())
        if not product_in_subcategory.exists():
            return Response({'response': {'code': '5', 'error': f'Subcategory not found'}}, status=400)
        for product in product_in_subcategory:
            products.append(product.name)

# 13a_6gQ3ABi9GrZT59yMLw
