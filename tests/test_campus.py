headers = {
    'Authorization': 123
}


def test_get_campus_list(client):
    response = client.get('/flaskeleton-api/campus/')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert response.json[0]['descricao'] == 'Campus Teste'


def test_get_campus(client):
    response = client.get('/flaskeleton-api/campus/1')
    assert response.status_code == 200
    assert response.json['descricao'] == 'Campus Teste'


def test_get_campus_not_found(client):
    response = client.get('/flaskeleton-api/campus/100')
    assert response.status_code == 404
    assert response.json['erro'] == "NAO_ENCONTRADO"


def test_post_campus_not_authorized(client):
    response = client.post('/flaskeleton-api/campus/', json={
        "descricao": "Campus 1"
    })
    assert response.status_code == 401
    assert response.json['erro'] == "NAO_AUTORIZADO"


def test_post_campus(client):
    response = client.post('/flaskeleton-api/campus/', headers=headers, json={
        "descricao": "Campus 1"
    })
    assert response.status_code == 201
    assert response.json['descricao'] == "Campus 1"


def test_post_campus_invalido(client):
    response = client.post('/flaskeleton-api/campus/', headers=headers, json={
        "teste": 123
    })
    assert response.status_code == 400
    assert response.json['erro'] == "ERRO_VALIDACAO"


def test_put_campus_not_authorized(client):
    response = client.put('/flaskeleton-api/campus/1', json={
        "descricao": "Campus 2"
    })
    assert response.status_code == 401
    assert response.json['erro'] == "NAO_AUTORIZADO"


def test_put_campus_not_found(client):
    response = client.put('/flaskeleton-api/campus/2', json={
        "descricao": "Campus 1"
    }, headers=headers)
    assert response.status_code == 404
    assert response.json['erro'] == "NAO_ENCONTRADO"


def test_put_campus(client):
    response = client.put('/flaskeleton-api/campus/1', json={
        "descricao": "Campus 1"
    }, headers=headers)
    assert response.status_code == 200
    assert response.json['descricao'] == "Campus 1"


def test_delete_campus_not_authorized(client):
    response = client.delete('/flaskeleton-api/campus/1')
    assert response.status_code == 401
    assert response.json['erro'] == "NAO_AUTORIZADO"


def test_delete_campus_not_found(client):
    response = client.delete('/flaskeleton-api/campus/2', headers=headers)
    assert response.status_code == 404
    assert response.json['erro'] == "NAO_ENCONTRADO"


def test_delete_campus(client):
    response = client.delete('/flaskeleton-api/campus/1', headers=headers)
    assert response.status_code == 204
    assert client.get('/flaskeleton-api/campus/1').status_code == 404
