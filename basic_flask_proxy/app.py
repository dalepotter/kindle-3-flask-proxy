import re
import requests
from urllib.parse import urlparse
from flask import request, Flask, Response

app = Flask(__name__.split('.')[0])


def convert_links(html, domain_called, proxy_prefix):
    # Handle absolute imports
    output = re.sub(
        r'([href|src]=)["\'](.*)//(.*)["\']',
        rf'\1"{proxy_prefix}\3"',
        html
    )

    # Handle relative imports
    output = re.sub(
        r'([href|src]=)["\']/(.*)["\']',
        rf'\1"{proxy_prefix}{domain_called}/\2"',
        output
    )
    return output


@app.route('/p/<path>', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def _proxy(path, *args, **kwargs):
    """Heavily inspired by: https://stackoverflow.com/a/36601467/2761030"""
    url = f"http://{path}"

    resp = requests.request(
        method=request.method,
        url=f"http://{path}",
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    html = convert_links(
        resp.content.decode("utf-8"),
        domain_called=urlparse(url).netloc,
        proxy_prefix=f"http://{request.host}/p/",
    )

    response = Response(html, resp.status_code, headers)
    return response
