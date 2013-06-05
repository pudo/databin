from datetime import datetime
from flask import url_for
from databin.core import db


class Paste(db.Model):
    __tablename__ = 'frame'

    id = db.Column(db.Integer, primary_key=True)
    source_ip = db.Column(db.Unicode())
    description = db.Column(db.Unicode())
    format = db.Column(db.Unicode())
    data = db.Column(db.Unicode())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, service, event, data):
        obj = cls()
        return obj

    @classmethod
    def by_hash(cls, hash):
        q = db.session.query(cls).filter_by(hash=hash)
        return q.first()

    def to_dict(self):
        return {
            'id': self.id,
            'source_ip': self.source_ip,
            'description': self.description,
            'format': self.format,
            'data': self.data,
            'created_at': self.created_at
        }

    @classmethod
    def all(cls):
        return db.session.query(cls)
