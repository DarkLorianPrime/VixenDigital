import inspect
import sys

from django.core.management import BaseCommand

from core.backend.elasticbackend import Model
from products import models


class Command(BaseCommand):
    def get_classes(self):
        for name, obj in inspect.getmembers(sys.modules[models.__name__]):
            if inspect.isclass(obj):
                if issubclass(obj, Model):
                    if obj().index.get_index().get("status") == 404:
                        obj().index.create_index()

    def handle(self, *args, **options):
        self.get_classes()
