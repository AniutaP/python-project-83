from page_analyzer.app import app


def test_index():
    client = app.test_client()
    response = client.get('/')
    assert response.data == b'Welcome to My project!'
