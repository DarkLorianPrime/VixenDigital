import datetime
import json
import uuid
from collections import OrderedDict

import pytz
import rest_framework
from django.utils.deprecation import MiddlewareMixin

from .models import Token


class TokenChecker(MiddlewareMixin):
    def process_request(self, request):
        if request.method == 'POST':
            token = Token.objects
            if not token.exists():
                token.create(token=uuid.uuid4().hex)
            old_token = token.first().expired.replace(tzinfo=None)
            if old_token >= datetime.datetime.now():
                token.update(token=uuid.uuid4().hex)
            tokens = request.POST
            if tokens.get('token') is not None:
                if token.filter(token=tokens['token']).exists():
                    request.access = True
                return
            request.access = False
            return
