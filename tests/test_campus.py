# testa se get_campus esta sendo executado
def test_get_campus(client):
    response = client.get('/flaskeleton/campus/')
    assert response is not None
