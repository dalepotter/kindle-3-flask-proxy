# Kindle 3 Flask Proxy

Basic Flask proxy to support accessing modern websites using the Amazon Kindle 3 built-in web browser.


## Installation

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=basic_flask_proxy.app
$ flask run
```

Requests can then be make to `http://localhost:5000/p/<URL HERE WITHOUT PROTOCOL>` - example `http://localhost:5000/p/www.google.com`


## Development

```
$ export FLASK_ENV=development
$ pip install -r requirements_dev.txt
```

### Tests

Can be run using pytest:

```
pytest
```
