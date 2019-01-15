from os import getenv

from flask import Flask, render_template
from app.db import db


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', 'mysql://root:my-secret-pw@192.168.12.222/spam')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    LOG_CONFIG = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'verbose': {
                'format': "[%(levelname)s] %(asctime)s - %(name)s - %(filename)s:%(lineno)d: %(message)s",
                "datefmt": "%Y-%m-%d %H:%M:%S"
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "level": getenv('LOG_LEVEL', 'INFO'),
                "formatter": "verbose",
                "stream": "ext://sys.stdout"
            }
        },
        "loggers": {
            "*": {
                "propagate": False,
                "handlers": ["console"]
            },
        },
        "root": {
            "level": getenv('LOG_LEVEL', 'INFO'),
            "handlers": [
                "console"
            ]
        }
    }


app = Flask(__name__)
db.init_app(app)


@app.route('/')
def root():
    return render_template('dashboard.html')
