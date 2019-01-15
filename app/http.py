import os
from os import getenv

from flask import Flask, render_template, jsonify, request
from sklearn.externals import joblib

from app.db import db, Processed

current_dir = os.path.dirname(__file__)

tfidf = joblib.load(os.path.join(current_dir, "tfidf.pkl"))
clf = joblib.load(os.path.join(current_dir, "svm.pkl"))


class Config(object):
    SQLALCHEMY_DATABASE_URI = getenv('SQLALCHEMY_DATABASE_URI', 'mysql://root:my-secret-pw@127.0.0.1/spam')
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

app.config.from_object(Config)

db.init_app(app)


@app.route('/')
def root():
    return render_template('dashboard.html')


@app.route('/api', methods=['POST'])
def is_spam():
    text = request.form.get("text")

    transform = tfidf.transform((text,))
    predict = clf.predict(transform)

    predict = bool(predict[0] == 1)

    label = 'spam' if predict else 'not spam'
    processed = Processed(text, label)
    db.session.add(processed)
    db.session.commit()

    return jsonify({
        "is_spam": predict
    })


@app.route('/processed')
def processed_view():
    page = request.args.get("page", "1")
    per_page = request.args.get("per_page", "50")

    page = int(page)
    per_page = int(per_page)

    pagination = Processed.query.order_by(
        Processed.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    return render_template('processed.html', pagination=pagination)
