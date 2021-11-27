from datetime import datetime
from app import db
import logging
logger = logging.getLogger(__name__)


class Leccion(db.Model):
    __tablename__ = 'lecciones'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    description = db.Column(db.String, nullable=True)
    icon = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True)
    deleted_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Leccion {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Leccion.query.all()

    @staticmethod
    def get_lesson_by_id(id):
        try:
            return Leccion.query.filter_by(id=id).first()
        except Exception as e:
            logger.error("Error al devolver la leccion solicitada %s" % str(e))


class Clase(db.Model):
    __tablename__ = 'clases'
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String)
    text = db.Column(db.Text)
    lesson = db.Column(db.Integer,
                       db.ForeignKey('lecciones.id'),
                       nullable=False,
                       default=0)
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

    @staticmethod
    def get_levels_by_lesson(lesson):
        try:
            return Clase.query.filter_by(lesson=lesson).distinct(Clase.level)
        except Exception as e:
            logger.error("Error al devolver la leccion solicitada %s" % str(e))

    @staticmethod
    def get_lesson(lesson, level, page):
        try:
            return Clase.query.filter_by(lesson=lesson).filter_by(level=level).filter_by(order=page).first()
        except Exception as e:
            logger.error("Error al devolver la leccion solicitada %s" % str(e))


class Evaluacion(db.Model):
    __tablename__ = 'evaluaciones'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text)
    pregunta1 = db.Column(db.Text)
    pregunta2 = db.Column(db.Text)
    pregunta3 = db.Column(db.Text, nullable=True)
    pregunta4 = db.Column(db.Text, nullable=True)
    respuesta = db.Column(db.Integer)
    lesson = db.Column(db.Integer,
                       db.ForeignKey('lecciones.id'),
                       nullable=False)
    level = db.Column(db.Integer)
    order = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Evaluacion {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_evaluacion(level, page, lesson):
        try:
            return Evaluacion.query.filter_by(lesson=lesson).filter_by(level=level).filter_by(order=page).first()
        except Exception as e:
            logger.error("Error al devolver las preguntas solicitada %s" % str(e))


class Resultado (db.Model):
    __tablename__ = 'resultados'
    id = db.Column(db.Integer, primary_key=True)
    lesson = db.Column(db.Integer,
                       db.ForeignKey('lecciones.id'),
                       nullable=False)
    level = db.Column(db.Integer)
    order = db.Column(db.Integer)
    results = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Resultado {self.id}>'

    def save(self):
        if not self.id:
            db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all():
        return Resultado.query.all()

    @staticmethod
    def get_result4lesson(lesson, page, level):
        resultado = {"lesson": lesson,
                     "page": page,
                     "level": level,
                     "success": 0,
                     "mistakes": 0}
        success = Resultado.query.filter_by(lesson=lesson).filter_by(level=level).filter_by(order=page).filter_by(results=True).count()
        mistakes = Resultado.query.filter_by(lesson=lesson).filter_by(level=level).filter_by(order=page).filter_by(results=False).count()

        resultado["success"]  = success
        resultado["mistakes"] = mistakes
        return resultado


    @staticmethod
    def get_lesson(lesson, page):
        try:
            return Resultado.query.filter_by(level=lesson).filter_by(order=page).first()
        except Exception as e:
            logger.error("Error al devolver la leccion solicitada %s" % str(e))
