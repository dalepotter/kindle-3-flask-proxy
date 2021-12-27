import responses
from basic_flask_proxy.app import app


def test_p_calls_url():
    """A call to the proxy route must return what the content of the specificed URL."""
    responses.add(
        responses.GET,
        "http://www.google.com",
        body="Mock Google homepage",
        status=200
    )

    with app.test_client() as client:
        result = client.get("/p/www.google.com")

    assert result.data.decode() == "Mock Google homepage"
    assert result.status_code == 200
