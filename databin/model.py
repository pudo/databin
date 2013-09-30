from datetime import datetime
from formencode import Schema, validators, Invalid, FancyValidator

from databin.core import db
from databin.util import make_key
from databin.parsers import get_parsers


class ValidFormat(FancyValidator):

    def _to_python(self, value, state):
        for key, name in get_parsers():
            if value == key:
                return value
        raise Invalid('Not a valid format', value, None)


class PasteSchema(Schema):
    description = validators.String(min=0, max=255)
    format = ValidFormat()
    force_header = validators.StringBool(empty=False)
    data = validators.String(min=10, max=255000)


class Paste(db.Model):
    __tablename__ = 'paste'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.Unicode())
    source_ip = db.Column(db.Unicode())
    description = db.Column(db.Unicode())
    format = db.Column(db.Unicode())
    data = db.Column(db.Unicode())
    force_header = db.Column(db.Boolean())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def create(cls, data, source_ip):
        obj = cls()
        data = PasteSchema().to_python(data)
        while True:
            obj.key = make_key()
            if cls.by_key(obj.key) is None:
                break
        obj.source_ip = source_ip
        obj.description = data.get('description')
        obj.format = data.get('format')
        obj.force_header = data.get('force_header')
        obj.data = data.get('data')
        db.session.add(obj)
        db.session.commit()
        return obj

    @classmethod
    def by_key(cls, key):
        q = db.session.query(cls).filter_by(key=key)
        return q.first()

    def to_dict(self):
        return {
            'id': self.id,
            'key': self.key,
            'source_ip': self.source_ip,
            'description': self.description,
            'format': self.format,
            'force_header': self.force_header,
            'data': self.data,
            'created_at': self.created_at
        }

    @classmethod
    def all(cls):
        return db.session.query(cls)

db.create_all()
