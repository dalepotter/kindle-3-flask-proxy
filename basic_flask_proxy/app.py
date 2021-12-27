import requests
from flask import request, Flask, Response

app = Flask(__name__.split('.')[0])


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

    response = Response(resp.content, resp.status_code, headers)
    return response
