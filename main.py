import json
import csv
from datetime import datetime


def find_by_key(iterable, key, value):
    """
    Поиск в списке словарей словаря с указанным ключом и значением.
    :param iterable: список или кортеж словарей
    :param key: искомый ключ
    :param value: искомое значение
    :return: кортеж с индексом найденного словаря и сам словарь; если такого словаря в списке нет, возвращает кортеж (-1, -1)
    """
    for index, dict_ in enumerate(iterable):
        if key in dict_ and dict_[key] == value:
            return index, dict_
    return -1, -1


with open('exam_results.csv', 'r', encoding='utf-8') as inp_file:
    students = csv.DictReader(inp_file)  # считываем файл
    best_scores = [] # финальный список словарей
    pattern = '%Y-%m-%d %H:%M:%S'  # шаблон строки для преобразования в datetime
    for stud in students:
        stud['best_score'] = int(stud.pop('score')) # меняем название ключа и делаем значение ключа целочисленным
        # проверяем, есть ли уже в финальном списке словарь с таким же email
        i, d = find_by_key(best_scores, 'email', stud['email'])
        if i != -1:
        # если словарь с таким email уже имеется, сравниваем оценки; если оценки равны, сравниваем даты
            if int(stud['best_score']) > (int(d['best_score'])) or \
                    (stud['best_score'] == d['best_score'] and
                     datetime.strptime(stud['date_and_time'], pattern) > datetime.strptime(d['date_and_time'], pattern)):
                best_scores.pop(i)
                best_scores.append(stud)
        else:
            best_scores.append(stud)
    best_scores.sort(key=lambda x: x['email'])

with open('best_scores.json', 'w') as out_file:
    json.dump(best_scores, out_file, indent=3)
