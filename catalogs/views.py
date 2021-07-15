from rest_framework.response import Response
from rest_framework.views import APIView
from transliterate import translit
from catalogs.models import Main_Categories, Sub_Categories
from extras.token_checker import token_checker

errors = [{'code': '0', 'error': 'already exists'}]


class Start_Page(APIView):
    def get(self, request):
        if not Main_Categories.objects.exists():
            return Response({'response': {'code': '4', 'error': 'anything not found'}}, status=400)
        return Response({"response": {'code': '2', 'object': Main_Categories.objects.values_list('slug', 'name')}},
                        status=200)

    @token_checker
    def post(self, request):
        new_category = request.GET['name'].capitalize()
        if Main_Categories.objects.filter(name=new_category).exists():
            return Response({'response': errors[0]}, status=400)
        slug_rep = translit(new_category, 'ru', reversed=True).replace("'", '').replace(" ", '_').lower()
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
        main_category = Main_Categories.objects.filter(slug=mainCategory).first()
        all_categories = Sub_Categories.objects.filter(main_category=main_category)
        if not all_categories.exists():
            return Response({'response': {'code': '4', 'error': f'Subcategories not found'}}, status=400)
        return Response({'response': {'code': '2', 'objects': Main_Categories.objects.values_list('slug', 'name')}})

    @token_checker
    def post(self, request, mainCategory):
        new_category = request.GET['name'].capitalize()
        main_category_model = Main_Categories.objects.filter(slug=mainCategory).first()
        all_categories = Sub_Categories.objects.filter(main_category=main_category_model)
        if all_categories.exists():
            return Response({'response': errors[0]}, status=400)
        slug_rep = translit(new_category, 'ru', reversed=True).replace("'", '').replace(" ", '_')
        Sub_Categories.objects.create(name=new_category, main_category=main_category_model, slug=slug_rep)
        return Response({'response': {'code': '1', 'object': new_category}}, status=200)


class Products(APIView):
    def get(self, request, mainCategory, subCategory):
        main_category = Main_Categories.objects.filter(name=mainCategory).first()
        product_in_subcategory = Sub_Categories.objects.filter(name=subCategory, main_category=main_category)
        if not product_in_subcategory.exists():
            return Response({'response': {'code': '5', 'error': f'Subcategory not found'}}, status=400)

# 13a_6gQ3ABi9GrZT59yMLw
