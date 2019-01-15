from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Processed(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)

    text = db.Column(db.String(10000), nullable=False)

    label = db.Column(db.String(500), nullable=False)

    create_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, text, label):
        self.text = text
        self.label = label
        self.create_on = datetime.now()
