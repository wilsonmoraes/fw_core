from http import HTTPStatus
#
from flask import jsonify, Blueprint
from werkzeug.exceptions import BadRequest

exception_handler_bp = Blueprint('errors', __name__)
import logging

logger = logging.getLogger()


@exception_handler_bp.app_errorhandler(Exception)
def handle_invalid_usage(e):
    logger.error(e, exc_info=True)
    error_code = HTTPStatus.INTERNAL_SERVER_ERROR
    error_description = "Internal server error"
    if isinstance(e, JWTError):
        error_description = e.error
        error_code = e.status_code
    # Se não colocar virgula - error, o exception volta no response.data e o correto é retornar response.error
    return json_obj_error(error_code, error_description), error_code


@exception_handler_bp.app_errorhandler(404)
def not_found_exception(err):
    """
    Fires a not found exception
    :param err:
    :return:
    """
    logger.error(err, exc_info=True)
    response = json_obj_error(HTTPStatus.NOT_FOUND, str(err))
    return response, 404


@exception_handler_bp.app_errorhandler(422)
def unprocessable_entity(err):
    """
    Fires a  unprocessable entity exception
    :param err:
    :return:
    """
    logger.error(err, exc_info=True)
    response = json_obj_error(HTTPStatus.UNPROCESSABLE_ENTITY, err.description)
    return response, 422


@exception_handler_bp.app_errorhandler(401)
def not_found_exception(err):
    """
    Fires a  unauthorized exception
    :param err:
    :return:
    """
    logger.error(err, exc_info=True)
    response = json_obj_error(HTTPStatus.UNAUTHORIZED, str(err))
    return response, 401


@exception_handler_bp.app_errorhandler(400)
def bad_request(err: BadRequest):
    """
    Fires a  unprocessable BadRequest exception
    :param err:
    :return:
    """
    logger.error(err, exc_info=True)
    response = json_obj_error(HTTPStatus.BAD_REQUEST, err.description)
    return response, 400


def json_obj_error(error_code, error_description):
    """
    Transforms errors in a standard way with description and code for handling in the front
    :param error_code:
    :param error_description:
    :return:
    """
    return jsonify(
        {"error_code": error_code, "error_description": error_description})


class JWTError(Exception):
    def __init__(self, error, status_code=HTTPStatus.UNAUTHORIZED):
        Exception.__init__(self)
        self.error = error
        self.status_code = status_code
