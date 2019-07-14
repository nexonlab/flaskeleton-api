# testa se get_campus esta sendo executado
def test_get_campus(client):
    response = client.get('/flaskeleton-api/campus/')
    assert response is not None


def test_get_campus_not_authorized(client):
    response = client.get('/flaskeleton-api/campus/')
    assert response is not None
    assert b'\"mensagem\": \"Missing authorization header.\"' in response.data
    
    response = client.get('/flaskeleton-api/campus/', headers={
        "Authorization": "abc"
    })
    assert response is not None
    assert b'\"mensagem\": \"Wrong authorization value.\"' in response.data


def test_get_campus_authorized(client):
    response = client.get('/flaskeleton-api/campus/', headers={
        "Authorization": "123"
    })
    assert response is not None

    response = client.get('/flaskeleton-api/campus/', headers={
        "Authorization": "123",
        "Context": "production"
    })
    assert response is not None
