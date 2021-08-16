from . import class_bp
from flask import jsonify, request
import logging
import flask
import psycopg2
from .models import Clase


logger = logging.getLogger(__name__)


@class_bp.route('/api/class')
def getAllProducts(*args, **kwargs):
    ret = []
    ret_code = 200

    try:
        results = Clase.get_all()
        for result in results:
            ret.append({"image": result.image,
                        "text": result.text,
                        "page": request.args.get('page'),
                        "total": str(len(results)),
                        "type": result.type})
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    # except Exception as e:
        # TODO: Cambiar por una entrada en el log
        print("Error de acceso a la base de datos " + str(error))
        ret_code = 404
        ret.append({"Error": "Error al realizar la consulta"})
    finally:
        return flask.make_response(jsonify(ret), ret_code)
