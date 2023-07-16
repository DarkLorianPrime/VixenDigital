class Field:
    name = None

    def __init__(self, null: bool = False):
        self.null = null


class TextField(Field):
    name = "text"


class IntegerField(Field):
    name = "integer"


class DateField(Field):
    name = "date"


class BooleanField(Field):
    name = "boolean"


class KeywordField(Field):
    name = "keyword"
    # name = {"type": "text", "fields": {"keyword": }}


class ObjectField(Field):
    def __init__(self, to):
        params = {}
        for key, element in to.__dict__.items():
            if isinstance(element, Field):
                params[key] = {"type": element.name}

        self.name = {"properties": params}