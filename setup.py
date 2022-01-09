from setuptools import setup, find_packages

setup(
    name='basic_flask_proxy',
    version='0.0.1',
    url='https://github.com/dalepotter/kindle-3-flask-proxy',
    author='Dale Potter',
    author_email='dalepotter@gmail.com',
    description='Basic Flask proxy to support accessing modern websites using the Amazon Kindle 3 built-in web browser.',
    packages=find_packages(),
    install_requires=[
        "Flask==2.0.2",
        "flask-wtf==1.0.0",
        "requests==2.26.0",
    ]
)
