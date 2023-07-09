import inspect
import os
import sys

from django.core.management import BaseCommand

from core.backend.elasticbackend import Model
from products import models


class Command(BaseCommand):
    def get_classes(self):
        for name, obj in inspect.getmembers(sys.modules[models.__name__]):
            if inspect.isclass(obj):
                if issubclass(obj, Model):
                    obj().index.recreate_index()

    def handle(self, *args, **options):
        self.get_classes()