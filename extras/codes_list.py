def codelist():
    code_list = [{'description': 'Объект уже зарегистрирован в базе', 'code': '0'},
                 {'description': 'Операция прошла успешно. POST методы', 'code': '1'},
                 {'description': 'Операция прошла успешно. GET методы', 'code': '2'},
                 {'description': 'Токен неверный', 'code': '3'},
                 {'description': 'Объектов этого раздела в базе нет', 'code': '4'},
                 {'description': 'Данного объекта в базе нет', 'code': '5'},
                 {'description': 'Переданы не все параметры', 'code': '6'}]
    return code_list