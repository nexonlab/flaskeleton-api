import simplejson
from flask import current_app
from ..models.db import db


def recupera_aluno(codigo=None):
    try:
        with open('./appmodels/data.json') as json_file:
            dados = simplejson.load(json_file)
        
        if codigo is not None:
            for aluno in dados:
                if aluno['codigo'] == codigo:
                    return aluno
        else:
            return dados
    except Exception as e:
        raise e
