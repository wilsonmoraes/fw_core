import datetime


class DateHelper:

    @staticmethod
    def str_to_date(date: str) -> datetime.date:
        return datetime.datetime.strptime(date.strip(), '%d/%m/%Y').date()

    @staticmethod
    def str_to_date_time(date_time: str) -> datetime:
        return datetime.datetime.strptime(date_time.strip(), '%d/%m/%Y %H:%M:%S')

    @staticmethod
    def date_to_str(date: datetime.date, date_format='%d/%m/%Y') -> str:
        return datetime.date.strftime(date, date_format)

    @staticmethod
    def date_time_to_str(date_time: datetime, date_time_format='%d/%m/%Y %H:%M:%S') -> str:
        return datetime.datetime.strftime(date_time, date_time_format)

    @staticmethod
    def date_to_date_time(date: datetime.date) -> datetime:
        return datetime.datetime.combine(date, datetime.datetime.min.time())

    @staticmethod
    def date_time_to_date(date_time: datetime.datetime) -> datetime.date:
        return date_time.date()
