from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import create_app, db


class User(db.Model, UserMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, nullable=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(256), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    #profile = db.relationship('Profile', backref='user', lazy='True')

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def save(self):
        try:
            
            if not self.id:
                db.session.add(self)
            db.session.commit()

        except SQLAlchemyError as e:
            #logger.error(e.args)
            session.rollback()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_by_id(id):
        return User.query.get(id)

    @staticmethod
    def get_by_email(email):
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            print("Error al acceder a la base de datos %s" % e)

    @staticmethod
    def get_all():
        return User.query.all()


class Profile(db.Model, UserMixin):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True, nullable=True)
    #company_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)
    company_id = db.Column(db.Integer, unique=True, nullable=False)
    size = db.Column(db.String(80), nullable=True)
    phone = db.Column(db.String(256), unique=True, nullable=False)
    ein = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(128), nullable=False)
    address2 = db.Column(db.String(128), nullable=False)
    country = db.Column(db.String(128), nullable=False)
    city = db.Column(db.String(128), nullable=False)
    state = db.Column(db.String(128), nullable=False)
    zipcode = db.Column(db.String(128), nullable=False)
    contact_name = db.Column(db.String(128), nullable=False)
    contact_phone = db.Column(db.String(128), nullable=True)
    contact_phone2 = db.Column(db.String(128), nullable=True)
    contact_email = db.Column(db.String(128), nullable=True)
    
    def save(self):
        print("Guardar")
        try:
            if not self.id:
                db.session.add(self)
            db.session.commit()
        
        except Exception as e:
            print("ERROR %s " % e)

    def update(user, profile):
        pass
    

    @staticmethod
    def get_my_profile(company_id):
        return Profile.query.filter_by(company_id=company_id).first()

    @staticmethod
    def delete_profile(company_id):
        Profile.query.filter_by(company_id=company_id).delete()
        db.session.commit()