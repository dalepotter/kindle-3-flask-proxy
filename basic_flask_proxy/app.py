import requests
import secrets
from flask import Flask, Response, redirect, render_template, request, url_for
from basic_flask_proxy.forms import EnterUrlForm
from basic_flask_proxy.utils import convert_links

app = Flask(__name__.split('.')[0])
app.secret_key = secrets.token_urlsafe(16)


@app.route('/', methods=['GET', 'POST'])
def index():
    form = EnterUrlForm()
    if form.validate_on_submit():
        return redirect(url_for("proxy", url=form.url.data))
    return render_template("index.html", form=form)


@app.route('/p', methods=['GET', 'POST', 'DELETE', 'PUT', 'PATCH'])
def proxy():
    """Heavily inspired by: https://stackoverflow.com/a/36601467/2761030"""
    url = request.args['url']
    url_with_scheme = f"http://{url}"

    resp = requests.request(
        method=request.method,
        url=url_with_scheme,
        headers={key: value for (key, value) in request.headers if key != 'Host'},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=True
    )

    excluded_headers = ['content-encoding', 'content-length', 'transfer-encoding', 'connection']
    headers = [(name, value) for (name, value) in resp.raw.headers.items()
               if name.lower() not in excluded_headers]

    try:
        resp_content = convert_links(
            resp.content.decode("utf-8"),
            current_url=url,
            proxy_prefix=f"http://{request.host}/p?url=",
        )
    except UnicodeDecodeError:
        resp_content = resp.content

    response = Response(resp_content, resp.status_code, headers)
    return response
