from django.core import serializers
from django.db.models.query import QuerySet
import json

def JsonSerialize(to_serialize):
    remove_from_array = False

    if type(to_serialize) is QuerySet:
        json_array = json.loads(serializers.serialize('json', to_serialize))
    else:
        remove_from_array = True
        json_array = json.loads(serializers.serialize('json', [to_serialize]))
    json_list = []
    print('array', json_array)
    for item in json_array:
        print('item', item)
        json_list.append(item['fields'])
    if remove_from_array:
        return json_list[0]
    else:
        return json_list

