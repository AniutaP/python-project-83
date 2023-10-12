from page_analyzer.app import app


def test_home():
    response = app.test_client().get('/')
    html = response.data.decode()
    assert response.status_code == 200
    assert '<a class="navbar-brand" href="/">Анализатор страниц</a>' in html
    assert '<a class="nav-link" href="/urls">Сайты</a>' in html
