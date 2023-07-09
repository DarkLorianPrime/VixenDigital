import os
import re

import httpx
from django.conf import settings
from httpx import BasicAuth

from core.backend.elasticfields import Field

default_path = "hits.hits._source"


class Index:
    def __init__(self, base: httpx.Client, index: str, structure: dict):
        self.base = base
        self.index = index
        self.structure = structure

    def create_index(self):
        return self.base.put(self.index,
                             json={
                                 "mappings": {
                                     "properties": {
                                         **self.structure
                                     }
                                 }
                             }).json()

    def get_index(self):
        result = self.base.get(self.index)
        if result.status_code == 404:
            return {"status": 404}

        return result.json()

    def remove_index(self):
        result = self.base.delete(self.index)
        if result.status_code == 404:
            return {"status": 404}

        return result.json()

    def recreate_index(self):
        self.remove_index()
        self.create_index()


class Aggregation:
    def __init__(self, search):
        self.aggregation = {"aggs": {}}
        self.search = search


class One:
    def __init__(self, name, field_name):
        self.aggs = {"aggs": {name: {"terms": {"field": field_name}}}}


class Many:
    def __init__(self, bucket, **kwargs):
        aggs_list = []
        for key, value in kwargs.items():
            aggs_list.append({key: {"terms": {"field": value}}})

        self.aggs = {"aggs": {bucket: {"composite": {"sources": aggs_list}}}}


class Result:
    def __init__(self, result):
        self.result = result
        self.source_ = {}
        self.aggregation = {}

    def parse(self):
        if self.result.get("status") == 400:
            raise Exception(self.result)
        hits = self.result.get("hits")
        if not hits:
            return {}

        self.source_ = [element["_source"] for element in self.result["hits"]["hits"]]
        self.aggregation = self.result.get("aggregation")

        return self.result["hits"], self.result.get("aggregations")


class Search:
    def __init__(self, base: httpx.Client, index: str, structure: dict):
        self.base = base
        self.index = index
        self.structure = structure
        self.aggs = {}
        self.sort_params = {"sort": []}
        self.size_param = {}
        self.return_params = []

    def return_(self, *args):
        params = []
        for i in args:
            params.append(f"{default_path}.{i}")

        self.return_params = {"filter_path": ",".join(params)}
        return self

    def size(self, size):
        self.size_param = {"size": size}
        return self

    def aggregation(self, aggregation_class):
        self.aggs = aggregation_class.aggs
        return self

    def post(self, json=None, params=None):
        result = self.base.post(f"{self.index}/_search/", json=json, params=params)
        return result.json()

    def get(self, params=None):
        result = self.base.get(f"{self.index}/_search/", params=params)
        return result.json()

    def all(self):
        body = {**self.size_param, "query": {"match_all": {}}, **self.aggs, **self.sort_params}
        params = self.return_params
        return Result(self.post(json=body, params=params))

    def script(self, **kwargs):
        key, element = None, None

        for key, element in kwargs.items():
            key, element = key, element

        return Result(self.get({**self.size_param, **self.aggs, **self.sort_params,
                                "script_fields": {key: {"script": {"source": element}}}}))

    def filter(self, **kwargs):
        filter_params = []

        for key, element in kwargs.items():
            filter_params.append({"term": {key: element}})

        body = {**self.size_param, "query": {"bool": {"filter": filter_params}}, **self.aggs, **self.sort_params}
        params = self.return_params
        return Result(self.post(json=body, params=params))

    def exists(self, exist_field, **kwargs):
        filter_params = []
        for key, element in kwargs.items():
            filter_params.append({"term": {key: element}})
        body = {**self.size_param, **self.aggs, **self.sort_params,
                "query": {"bool": {"must": [{"exists": {"field": exist_field}, "filter": filter_params}]}}}
        return Result(self.post(json=body))

    def in_(self, **kwargs):
        if not kwargs:
            return None

        params = list(*kwargs.items())
        return Result(self.post({**self.size_param, "query":
            {"query_string":
                 {"query": params[1], "default_field": params[0]}}, **self.aggs, **self.sort_params}))

    def sort(self, **sort_fields):
        for key, value in sort_fields:
            self.sort_params["sort"].append({key: value})


class Model:
    host = getattr(settings, "ELASTIC_HOST", os.getenv("ELASTIC_HOST"))
    port = getattr(settings, "ELASTIC_PORT", os.getenv("ELASTIC_PORT"))
    user = getattr(settings, "ELASTIC_USER", os.getenv("ELASTIC_USER"))
    password = getattr(settings, "ELASTIC_PASSWORD", os.getenv("ELASTIC_PASSWORD"))

    if not host or not port or not user or not password:
        raise Exception("Elastic params will be not None")

    base = httpx.Client(base_url=f"http://{host}:{port}/",
                        verify=False,
                        auth=BasicAuth(username=user, password=password))

    def __init__(self):
        self.__params = {}
        self.index = Index(self.base, self._index, self.get_structure())

    def get_structure(self):
        for key, element in self.__class__.__dict__.items():
            if isinstance(element, Field):
                if isinstance(element.name, str):
                    self.__params[key] = {"type": element.name}
                else:
                    self.__params[key] = element.name
        return self.__params

    @property
    def _index(self):
        return f"{self.__class__.__name__.lower()}_index"

    @property
    def objects(self) -> Search:
        return Search(self.base, self._index, self.get_structure())

    def __call__(self, **kwargs):
        need_items = self.get_structure()
        elements = {}
        for key, element in need_items.items():
            new_element = kwargs.pop(key, None)
            if new_element is None:
                raise Exception(f"\"{key}\" - обязательный параметр")
            regex = ""
            if element.get("type") == "text":
                regex = r"^[\S _-]+$"

            if element.get("type") == "integer":
                regex = r"^\d+$"

            d = re.match(regex, str(new_element))

            if not d:
                raise Exception(f"У поля \"{key}\" должен быть тип {element.get('type')}")

            elements[key] = new_element

        return self.base.post(f"{self._index}/_doc", json=elements).json()
