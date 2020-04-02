def test_get_docs(client):
    response = client.get('/flaskeleton-api/apidocs/')
    assert response is not None
