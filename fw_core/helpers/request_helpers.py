from flask import request, jsonify


def request_to_data() -> dict:
    """create dict with parameters from query string

    :return: dict
    """
    params = request.args.to_dict()
    if params is None:
        params = {}

    data = dict()
    for key in params:
        data['{}'.format(str(key))] = params[key]
    return data


def create_header_location(location: str):
    """
    Metodo criado pra  incluir um cabeçalho Location que aponte para o URL do novo objeto
    :param location:
    :return:
    """
    response = jsonify()
    response.status_code = 201
    response.headers['location'] = location
    return response
