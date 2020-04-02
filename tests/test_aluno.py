headers = {
    'Authorization': 123
}


def test_get_alunos_list(client):
    response = client.get('/flaskeleton-api/aluno/')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json[0]['nome'] == 'Joao da Silva'


def test_get_aluno(client):
    response = client.get('/flaskeleton-api/aluno/1')
    assert response.status_code == 200
    assert response.json['nome'] == "Joao da Silva"


def test_get_aluno_not_found(client):
    response = client.get('/flaskeleton-api/aluno/100')
    assert response.status_code == 404
    assert "NAO_ENCONTRADO" == response.json['erro']


def test_post_aluno_not_authorized(client):
    data = {
        "nome": "Jose Sousa",
        "email": "josesousa@email.com",
        "endereco": "Rua da Felicidade, 1 - Aguas Claras"
    }
    response = client.post('/flaskeleton-api/aluno/', json=data)
    assert response.status_code == 401
    assert response.json['erro'] == 'NAO_AUTORIZADO'


def test_post_aluno(client):
    data = {
        "nome": "Jose Sousa",
        "email": "josesousa@email.com",
        "endereco": "Rua da Felicidade, 1 - Aguas Claras"
    }
    response = client.post('/flaskeleton-api/aluno/', json=data, headers=headers)
    assert response.status_code == 201
    assert response.json == {
        "codigo": 2,
        "nome": "Jose Sousa",
        "email": "josesousa@email.com",
        "endereco": "Rua da Felicidade, 1 - Aguas Claras"
    }


def test_post_aluno_invalido(client):
    data = {
        "teste": 123
    }
    response = client.post('/flaskeleton-api/aluno/', json=data, headers=headers)
    assert response.status_code == 400
    assert response.json['erro'] == "ERRO_VALIDACAO"


def test_put_aluno_not_authorized(client):
    data = {
        "nome": "Jose Sousa",
        "email": "josesousa@email.com",
        "endereco": "Rua da Felicidade, 20"
    }
    response = client.post('/flaskeleton-api/aluno/', json=data)
    assert response.status_code == 401
    assert response.json['erro'] == 'NAO_AUTORIZADO'


def test_put_aluno(client):
    data = {
        "nome": "Jose Sousa",
        "email": "josesousa@email.com",
        "endereco": "Rua da Felicidade, 20"
    }
    response = client.post('/flaskeleton-api/aluno/', json=data, headers=headers)
    assert response.status_code == 201
    assert response.json["endereco"] == "Rua da Felicidade, 20"


def test_delete_aluno_not_authorized(client):
    response = client.delete('/flaskeleton-api/aluno/1')
    assert response.status_code == 401
    assert response.json['erro'] == 'NAO_AUTORIZADO'


def test_delete_aluno(client):
    assert client.delete('/flaskeleton-api/aluno/1', headers=headers).status_code == 204
    assert client.get('/flaskeleton-api/aluno/1', headers=headers).status_code == 404


def test_delete_aluno_not_found(client):
    response = client.delete('/flaskeleton-api/aluno/100', headers=headers)
    assert response.status_code == 404
    assert "NAO_ENCONTRADO" == response.json['erro']


def test_get_list_alunos(client):
    data = {
        "nome": "Jose Sousa",
        "email": "josesousa@email.com",
        "endereco": "Rua da Felicidade, 1 - Aguas Claras"
    }
    client.post('/flaskeleton-api/aluno/', json=data, headers=headers)
    response = client.get('/flaskeleton-api/aluno/')
    assert [aluno['codigo'] for aluno in response.json] == [1, 2]
