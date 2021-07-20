from rest_framework.response import Response

from catalogs.models import Access_Token


def token_checker(fn):
    def wrapper(*args, **kwargs):
        if not Access_Token.objects.filter(token=args[1]['name']).exists():
            return Response({'response': {'code': '3', 'error': 'token not found'}}, status=400)
        return fn(*args, **kwargs)

    return wrapper
