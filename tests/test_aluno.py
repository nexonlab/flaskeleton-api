# testa a recuperacao da lista de alunos
def test_get_alunos(client):
    response = client.get('/flaskeleton-api/aluno/')
    assert response is not None
    assert response.status_code == 200


def test_get_aluno(client):
    response = client.get('/flaskeleton-api/aluno/1')
    assert response is not None
    assert b"\"codigo\": 1" in response.data


def test_get_aluno_empty(client):
    response = client.get('/flaskeleton-api/aluno/100')
    assert response is not None
    assert b"{}" in response.data
