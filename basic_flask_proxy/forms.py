from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import Regexp


class EnterUrlForm(FlaskForm):
    url = StringField(
        'Enter URL to visit',
        validators=[
            Regexp(
                regex=r'^[A-Za-z0-9][A-Za-z0-9.-]+(:\d+)?(/.*)?$',  # Credit https://stackoverflow.com/a/971094/2761030
                message='Enter a valid domain (without scheme prefix) - like \'example.com\''
            ),
        ]
    )
