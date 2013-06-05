from datetime import datetime
from formencode import Schema, validators

from databin.core import db
from databin.util import encode, decode


class PasteSchema(Schema):
    description = validators.String(min=0, max=255)
    #format = validators.String(min=3, max=255)
    data = validators.String(min=10, max=255000)


class Paste(db.Model):
    __tablename__ = 'frame'

    id = db.Column(db.Integer, primary_key=True)
    source_ip = db.Column(db.Unicode())
    description = db.Column(db.Unicode())
    format = db.Column(db.Unicode())
    data = db.Column(db.Unicode())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def key(self):
        return encode(self.id)

    @classmethod
    def create(cls, data, source_ip):
        obj = cls()
        data = PasteSchema().to_python(data)
        obj.source_ip = source_ip
        obj.description = data.get('description')
        obj.format = data.get('format')
        obj.data = data.get('data')
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def by_key(cls, key):
        q = db.session.query(cls).filter_by(id=decode(key))
        return q.first()

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'source_ip': self.source_ip,
            'description': self.description,
            'format': self.format,
            'data': self.data,
            'created_at': self.created_at
        }

    @classmethod
    def all(cls):
        return db.session.query(cls)

db.create_all()
