from datetime import datetime, date

from flask import abort


class BusinessValidation:

    @staticmethod
    def less_than_or_equal_zero(param, lbl_start):
        if not param or param <= 0:
            BusinessValidation.abort_422("{} deve ser informada".format(lbl_start))

    @staticmethod
    def date_time_is_before_today(date_time_param: datetime, lbl_start):
        if not date_time_param or date_time_param < datetime.now():
            BusinessValidation.abort_422("A data {} não pode ser menor que a data atual".format(lbl_start))

    @staticmethod
    def date_is_before_today(date_param: date, lbl_start):
        if not date_param or date_param < date.today():
            BusinessValidation.abort_422("A data {} não pode ser menor que a data atual".format(lbl_start))

    @staticmethod
    def start_is_after_end(start: datetime, end: datetime, lbl_start, lbl_end):
        if not start or not end or start < end:
            BusinessValidation.abort_422("A data {} não pode ser maior que a data {}".format(lbl_start, lbl_end))

    @staticmethod
    def required(obj: dict, *fields_requireds: str):
        """
        Fires a error(400) if anyone property of fields_requireds not exist into dickt
        :param fields_requireds:
        :param obj:
        :return:
        """
        err_msg: str = '\'{}\' cannot be null or null'
        for field in fields_requireds:
            fild_splited: [str] = field.split('.')
            first, rest = fild_splited[0], fild_splited[1:]
            if rest:
                BusinessValidation.required(obj[first], *rest)
            else:
                if field not in obj:
                    BusinessValidation.abort_422(err_msg.format(field))
                elif isinstance(obj.get(field), str) and not obj.get(field):  # string vazia
                    BusinessValidation.abort_422(err_msg.format(field))
                elif isinstance(obj.get(field), list) and len(obj.get(field)) == 0:  # lista vazia
                    BusinessValidation.abort_422(err_msg.format(field))

    @staticmethod
    def abort_if(condition: bool, msg: str):
        if condition:
            BusinessValidation.abort_422(msg=msg)

    @staticmethod
    def abort_422(msg: str = None):
        abort(422, description=msg)
