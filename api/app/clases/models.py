from datetime import datetime
from app import db
import logging
logger = logging.getLogger(__name__)


class Clase(db.Model):
    __tablename__ = 'clases'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    text = db.Column(db.Text)
    level = db.Column(db.Integer)
    type = db.Column(db.Integer)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Clase.query.all()
