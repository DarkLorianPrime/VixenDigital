from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import resolve
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from catalogs.repositories import CategoryRepository

service = CategoryRepository()


class CategoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest, *args, **kwargs):
        _, _, kwargs = resolve(request.path)
        if kwargs:
            catalog: str = kwargs.get("catalog")
            category: str = kwargs.get("category")
            if not catalog and not category:
                response = self.get_response(request)

                return response

            handler = service.get_catalog if not category else service.get_category

            category = handler(catalog, category)

            if not category:
                return HttpResponseNotFound('{"detail": "Not found."}', content_type="application/json")

            request.category = category

        response = self.get_response(request)

        return response
