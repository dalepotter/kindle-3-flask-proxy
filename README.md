# Flask Proxy for the Kindle Keyboard (3rd generation) Web Browser

Users of the Kindle 'experimental' web browser may recognaise this message:

![kindle_screen_shot-64243-1](https://user-images.githubusercontent.com/8247168/159578703-3f3b416e-6b75-483b-92dc-2495d8c576e5.gif)

The source of the error message seems to be [outdated SSL certificates on the device](https://www.reddit.com/r/kindle/comments/lxh3d8/any_way_around_this_secure_connection_error_i). Whilst some users suggest the certificates can be [updated manually](https://www.mobileread.com/forums/showthread.php?t=254808), though this may require jailbroken device.

An alternative is to use a proxy to support accessing modern websites using the Amazon Kindle 3 built-in web browser.

This repo provides a proxy written in Flask.  Can be deployed to a PaaS (such as Heroku) to enable your own personal workaround.

**IMPORTANT:** This is (currently) a primitive proxy with many faults, but it will open up more sites than are currently accessible without it.  It should not be used for sending/viewing any sensitive data.


## Installation

```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
$ export FLASK_APP=basic_flask_proxy.app
$ flask run
```

Requests can then be make to `http://localhost:5000/p?url=<URL HERE WITHOUT PROTOCOL>` - example `http://localhost:5000/p?url=www.google.com`


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
