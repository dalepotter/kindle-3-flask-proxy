import re
import requests
import secrets
from urllib.parse import urljoin
from flask import Flask, Response, redirect, render_template, request, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__.split('.')[0])
app.secret_key = secrets.token_urlsafe(16)


class EnterUrlForm(FlaskForm):
    url = StringField('Enter URL to visit')


def convert_links(html, current_url, proxy_prefix):
    """Find and replace attribute references to URLs, so that they are prefixed by the proxy URL.
    Supports action/content/href/src attributes.

    Input:
        html (str) -- HTML content for the page.
        current_url (str) -- The current URL (without scheme) of the input HTML.
        proxy_prefix (str) -- The proxy URL that can be called to make requests and return content.

    Returns:
        str -- HTML content with attribute URL references prefixed with the proxy URL.
    """

    # Handle absolute URLs
    output = re.sub(
        r'([action|content|href|src]=)["\'](.*)//(.*)["\']',
        rf'\1"{proxy_prefix}\3"',  # Normalises all URL encapsulation to double quotes
        html
    )

    # Handle relative URLs
    def rel_url_to_proxy_replace(matchobj):
        """Return the absolute path to the a relative URL, prefixed by the proxy URL.

        Input:
            matchobj (re.Match) -- A regex match object.

        Returns:
            str -- Referenced URL, prefixed by the proxy URL.
        """
        absolute_url = urljoin(f"//{current_url}", matchobj.group(2))
        return f'{matchobj.group(1)}"{proxy_prefix}{absolute_url[2:]}"'  # Normalises all URL encapsulation to double quotes

    output = re.sub(
        r'([action|content|href|src]=)["\']([./]+.*)["\']',
        rel_url_to_proxy_replace,
        output
    )
    return output


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
