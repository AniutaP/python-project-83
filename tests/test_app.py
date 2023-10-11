from page_analyzer.app import app


def test_home():
    response = app.test_client().get('/')
    assert response.status_code == 200


def test_urls_table():
    response = app.test_client().get('/urls')
    assert response.status_code == 200