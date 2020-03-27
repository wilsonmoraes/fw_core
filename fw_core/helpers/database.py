# from app import db
from abc import abstractmethod

from flask_sqlalchemy import SQLAlchemy


class BaseModel:

    @classmethod
    @abstractmethod
    def alchemy_db(cls) -> SQLAlchemy:
        raise NotImplementedError

    @classmethod
    def find_by_id(cls, id_param: int):
        """
        Method that should be used to query an object in the database by passing the id, since the 'id' property exists by default.
        EX.:
        MyClass.get_by(name = 'some name')
        :param id_param:
        :return: o primeiro ítem
        """
        return cls.alchemy_db().session.query(cls).filter_by(id=id_param).first()

    @classmethod
    def refresh(cls, obj):
        """
        Updates the attributes attributes of the object passed by parameter.
        :param obj:
        :return:
        """
        cls.alchemy_db().session.refresh(cls, obj)  # refresh model from database

    @classmethod
    def delete(cls, obj):
        """
        removes the object
        :param obj: entidade
        """
        cls.alchemy_db().session.delete(obj)

    @classmethod
    def delete_by_id(cls, id_param):
        """
        removes the object by id
        :param id_param: entidade
        """
        obj = cls.find_by_id(id_param=id_param)
        cls.alchemy_db().session.delete(obj)

    @classmethod
    def save(cls, model):
        """
        insert or update model into database
        :param model: entidade
        """
        if model.id:
            cls.alchemy_db().session.merge(model)
        else:
            cls.alchemy_db().session.add(model)

        cls.alchemy_db().session.flush()  # after flush(), parent object would be automatically  assigned with a unique primary key to its id field
