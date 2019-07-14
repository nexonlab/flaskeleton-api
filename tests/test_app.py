def test_get_app(client):
    response = client.get('/flaskeleton-api/')
    assert response is not None


def test_get_invalid_route(client):
    response = client.get('/')
    assert response is not None
    assert b'Esta URL nao pertence a aplicacao' in response.data
