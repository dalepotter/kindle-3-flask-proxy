import pytest
import responses
from basic_flask_proxy.app import app, convert_links


@pytest.mark.parametrize("html_element_attribute", ["action", "content", "href", "src"])
@pytest.mark.parametrize("quote_char", ["\"", "'"])
@pytest.mark.parametrize("input_url, expected_output", [
    ("http://www.example.com/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("https://www.example.com/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("//www.example.com/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("../abc.py", "http://www.proxy.com/p?url=www.example.com/path/abc.py"),
    ("./abc.py", "http://www.proxy.com/p?url=www.example.com/path/to/abc.py"),
])
def test_convert_links(html_element_attribute, quote_char, input_url, expected_output):
    current_url = "www.example.com/path/to/file.txt"
    input_string = f'{html_element_attribute}={quote_char}{input_url}{quote_char}'

    result = convert_links(input_string, current_url, proxy_prefix="http://www.proxy.com/p?url=")

    assert result == f'{html_element_attribute}="{expected_output}"'


def test_index_get():
    """A GET request to the index page must return a 200 code and template content."""
    with app.test_client() as client:
        result = client.get("/")

    assert result.status_code == 200
    assert "<h1>Proxy for Kindle 3 web browser</h1>" in result.data.decode()


def test_index_post_valid():
    """A POST request to the index page must redirect to the expected proxy route."""
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False

    with app.test_client() as client:
        result = client.post("/", data={'url': "example.com"})

    assert result.status_code == 302
    assert result.location.endswith("/p?url=example.com")


def test_p_calls_url():
    """A call to the proxy route must return what the content of the specificed URL."""
    responses.add(
        responses.GET,
        "http://www.example.com",
        body="Mock web page",
        status=200
    )

    with app.test_client() as client:
        result = client.get("/p?url=www.example.com")

    assert result.data.decode() == "Mock web page"
    assert result.status_code == 200
