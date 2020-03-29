import datetime
import inspect
import json
from contextlib import suppress

from flask import jsonify
from sqlalchemy.engine import RowProxy

from fw_core.helpers.database import BaseModel
from fw_core.helpers.date_helpers import DateHelper


class ObjectMapper:

    @staticmethod
    def jsonify_schemaless(result: str, make_list: bool = False):
        if result:
            json_object = ObjectMapper.make_str_json_to_object(result)
            return jsonify(json_object)
        elif make_list:
            return jsonify([])
        return jsonify({})

    @staticmethod
    def jsonify(obj, ignore_properties: [str] = []):
        return jsonify(ObjectMapper.to_dict(obj, ignore_properties))

    @staticmethod
    def to_dict(obj, ignore_properties: [str] = []):
        """ Converte um objeto ou uma lista de objetos para json
        :param ignore_properties:
        :param obj:  objeto a ser convertido
        :return: retorna um json
        """
        if isinstance(obj, list):
            return [ObjectMapper.obj_to_dict(m, ignore_properties=ignore_properties) for m in obj]
        else:
            return ObjectMapper.obj_to_dict(obj, ignore_properties=ignore_properties)

    @staticmethod
    def make_str_json_to_object(result):
        """
        Método criado pra converter o binário 0 e 1 do mysql pra boolean.
        Sempre que escrever uma sql nativa, ela deve retornar uma string do tipo "true" ou "false"
        :param result:
        :return:
        """
        json_object = json.loads(result) if isinstance(result, str) else result
        if isinstance(json_object, list):
            json_object = [ObjectMapper.obj_to_dict(obj=item) for item in json_object]
        else:
            json_object = ObjectMapper.obj_to_dict(obj=json_object)

        return json_object

    @staticmethod
    def obj_to_dict(obj, ignore_properties: [str] = None):
        """ Converte um objeto para json
        :param ignore_properties:
        :param obj:objeto a ser convertido
        :return: um objeto no formado json
        """
        obj_response = {}

        obj = ObjectMapper.row_to_dict(obj, ignore_properties=ignore_properties)
        if obj:
            for key, value in obj.items():
                # if ignore_properties and len(ignore_properties) and key in ignore_properties:
                #    continue
                if isinstance(value, list):
                    obj_array = []
                    for item in value:
                        if isinstance(item, dict) or isinstance(item, RowProxy):
                            obj_array.append(ObjectMapper.obj_to_dict(obj=item))
                        else:
                            obj_array.append(item)
                    obj_response[key] = obj_array
                elif isinstance(value, str) and "true" == value.lower():
                    obj_response[key] = True
                elif isinstance(value, str) and "false" == value.lower():
                    obj_response[key] = False
                elif isinstance(value, datetime.datetime):
                    obj_response[key] = DateHelper.date_time_to_str(value)
                elif isinstance(value, datetime.date):
                    obj_response[key] = DateHelper.date_to_str(value)
                elif isinstance(value, BaseModel):
                    obj_response[key] = ObjectMapper.to_dict(obj=value)
                elif isinstance(value, bytes):
                    obj_response[key] = value.decode('utf-8')
                else:
                    obj_response[key] = value
        return obj_response

    @staticmethod
    def row_to_dict(row, ignore_properties: [] = None):
        d = {}

        if row is None:
            return None
        if isinstance(row, RowProxy):
            for column, value in row.items():
                # build up the dictionary
                d = {**d, **{column: value}}
        elif isinstance(row, dict):
            d = row
        elif not hasattr(row, '__dict__'):
            # is_primitive
            return row
        else:
            for c in inspect(row).attrs.keys():
                # build up the dictionary
                d = {**d, **{c: ObjectMapper.row_to_dict(getattr(row, c))}}

        if ignore_properties and len(ignore_properties):
            for prop in ignore_properties:
                removeproperty: [str] = prop.split('.')
                d = ObjectMapper.remove_property_from_dict_recursively(d, removeproperty)
        return d

    @staticmethod
    def remove_property_from_dict_recursively(dic, maplist):
        """
        Remove a propriedade recursivamente
        :param dic:
        :param maplist:
        :return:
        """
        first, rest = maplist[0], maplist[1:]

        if rest:
            # if `rest` is not empty, run the function recursively
            dic[first] = ObjectMapper.remove_property_from_dict_recursively(dic[first], rest)
        else:
            with suppress(KeyError):
                del dic[first]
        return dic


