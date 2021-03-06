import pytest
import responses
from urllib.parse import quote_plus
from basic_flask_proxy.app import app


@pytest.fixture()
def mock_app():
    """Return a mock instance of the app."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app


def test_index_get(mock_app):
    """A GET request to the index page must return a 200 code and template content."""
    with mock_app.test_client() as client:
        result = client.get("/")

    assert result.status_code == 200
    assert "<h1>Proxy for Kindle 3 web browser</h1>" in result.data.decode()


@pytest.mark.parametrize("valid_data", [
    "example.com", "subdomain.example.com:8080/path/to/file?url=param"
])
def test_index_post_valid(mock_app, valid_data):
    """A POST request to the index page (with VALID data) must redirect to the expected proxy route."""
    encoded_url = quote_plus(valid_data)

    with mock_app.test_client() as client:
        result = client.post("/", data={'url': valid_data})

    assert result.status_code == 302
    assert result.location.endswith(f"/p?url={encoded_url}")


@pytest.mark.parametrize("invalid_data", [
    "", " ", "not_a_domain", "http://example.com", "https://example.com", "//example.com"
])
def test_index_post_invalid(mock_app, invalid_data):
    """A POST request to the index page (with INVALID data) must display an error message."""
    with mock_app.test_client() as client:
        result = client.post("/", data={'url': invalid_data})

    assert result.status_code == 200
    assert "Enter a valid domain (without scheme prefix) - like &#39;example.com&#39;" in result.data.decode()


def test_p_calls_url(mock_app):
    """A call to the proxy route must return what the content of the specificed URL."""
    responses.add(
        responses.GET,
        "http://www.example.com",
        body="Mock web page",
        status=200
    )

    with mock_app.test_client() as client:
        result = client.get("/p?url=www.example.com")

    assert result.data.decode() == "Mock web page"
    assert result.status_code == 200
