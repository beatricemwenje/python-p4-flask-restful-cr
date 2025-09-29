from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Newsletter(db.Model):
    __tablename__ = 'newsletters'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    body = db.Column(db.String, nullable=False)
    published_at = db.Column(db.DateTime, server_default=db.func.now())
    edited_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__(self):
        return f'<Newsletter {self.title}, published at {self.published_at}.>'

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "published_at": self.published_at.isoformat() if self.published_at else None,
            "edited_at": self.edited_at.isoformat() if self.edited_at else None,
        }
