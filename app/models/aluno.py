from .db import db, ma
from sqlalchemy import Column, Integer, String
from marshmallow import fields


class Aluno(db.Model):

    __tablename__ = 'ALUNOS'

    codigo = Column(Integer, name='CODIGO', primary_key=True)
    nome = Column(String, name='NOME')
    email = Column(String, name='EMAIL')
    endereco = Column(String, name='ENDERECO')

    def dict_to_object(self, d: dict):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                if b:
                    setattr(self, a, [Aluno(x) if isinstance(x, dict) else x for x in b])
            else:
                if b:
                    setattr(self, a, Aluno(b) if isinstance(b, dict) else b)

    def __repr__(self):
        return "<Aluno codigo={codigo}, nome={nome}, email={email}>".format(codigo=self.codigo,
                                                                            nome=self.nome,
                                                                            email=self.email)


class AlunoSchema(ma.ModelSchema):
    class Meta:
        strict = True

    codigo = fields.Integer()
    nome = fields.String()
    email = fields.String()
    endereco = fields.String()
