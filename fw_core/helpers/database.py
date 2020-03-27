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
        Metodo que deve ser usado pra consultar um objeto no banco de dados passando o id, dado que a propriedade
        'id' exista por padrão.
        EX.:
        MyClass.get_by(name = 'some name')
        :param id_param:
        :return: o primeiro ítem
        """
        return cls.alchemy_db().session.query(cls).filter_by(id=id_param).first()

    @classmethod
    def refresh(cls, obj):
        """
        Atualiza os atributos attributos do objeto passado por parametro.
        :param obj:
        :return:
        """
        cls.alchemy_db().session.refresh(cls, obj)  # refresh model from database

    @classmethod
    def delete(cls, obj):
        """
        Remove o objeto
        :param obj: entidade
        """
        cls.alchemy_db().session.delete(obj)

    @classmethod
    def delete_by_id(cls, id_param):
        """
        Remove o objeto
        :param id_param: entidade
        """
        obj = cls.find_by_id(id_param=id_param)
        cls.alchemy_db().session.delete(obj)

    @classmethod
    def save(cls, model):
        """
        insere ou atualiza objeto no banco
        :param model: entidade
        """
        if model.id:
            cls.alchemy_db().session.merge(model)
        else:
            cls.alchemy_db().session.add(model)

        cls.alchemy_db().session.flush()  # after flush(), parent object would be automatically  assigned with a unique primary key to its id field
