from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponseNotFound, HttpResponse
from django.urls import resolve
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from catalogs.service import Service

service = Service()


class CategoryMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: WSGIRequest, *args, **kwargs):
        _, _, kwargs = resolve(request.path)
        if kwargs:
            catalog = kwargs.get("catalog")
            category = kwargs.get("category")

            handler = service.get_category
            if not category:
                handler = service.get_catalog

            category = handler(catalog, category)

            if not category:
                return HttpResponseNotFound('{"detail": "Not found."}', content_type="application/json")

            request.category = category

        response = self.get_response(request)

        return response
