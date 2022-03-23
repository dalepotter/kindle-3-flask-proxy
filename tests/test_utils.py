import pytest
from basic_flask_proxy.utils import convert_links


@pytest.mark.parametrize("html_element_attribute", ["action", "content", "href", "src"])
@pytest.mark.parametrize("quote_char", ["\"", "'"])
@pytest.mark.parametrize("input_url, expected_output", [
    ("http://www.example.com/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("https://www.example.com/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("//www.example.com/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("/path/to/file.jpg", "http://www.proxy.com/p?url=www.example.com/path/to/file.jpg"),
    ("../abc.py", "http://www.proxy.com/p?url=www.example.com/path/abc.py"),
    ("./abc.py", "http://www.proxy.com/p?url=www.example.com/path/to/abc.py"),
    (
        "http://www.example.com/wiki/Free_content\">free</a> <a href=\"http://www.example.com/wiki/Encyclopedia",
        "http://www.proxy.com/p?url=www.example.com/wiki/Free_content\">free</a> <a href=\"http://www.proxy.com/p?url=www.example.com/wiki/Encyclopedia"
    ),  # Multiple (absolute) links in the same line
    (
        "/wiki/Free_content\">free</a> <a href=\"/wiki/Encyclopedia",
        "http://www.proxy.com/p?url=www.example.com/wiki/Free_content\">free</a> <a href=\"http://www.proxy.com/p?url=www.example.com/wiki/Encyclopedia"
    )  # Multiple (relative) links in the same line
])
def test_convert_links(html_element_attribute, quote_char, input_url, expected_output):
    current_url = "www.example.com/path/to/file.txt"
    input_string = f'{html_element_attribute}={quote_char}{input_url}{quote_char}'

    result = convert_links(input_string, current_url, proxy_prefix="http://www.proxy.com/p?url=")

    assert result == f'{html_element_attribute}="{expected_output}"'
