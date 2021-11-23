from . import class_bp
from flask import jsonify, request
import logging
import flask
import psycopg2
from .models import Clase, Evaluacion, Leccion

logger = logging.getLogger(__name__)


@class_bp.route('/api/lessons', methods=['GET'])
def getLessons(*args, **kwargs):

    ret = []
    ret_code = 400
    logger.info("Devolver todas las lecciones")

    try:
        results = Leccion.get_all()
        if results is not None:

            for result in results:
                ret.append({"id": result.id,
                            "title": result.title,
                            "description": result.description,
                            "icon": result.icon,
                            "created_at": result.created_at,
                            "update_at": result.updated_at
                            })
            ret_code = 200
        else:
            logger.error("No hay más lecciones para %s" %
                         request.args.get('level'))

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error al recuperar la lección %s" % str(error))
        ret_code = 404
        ret.append({"Error": "Error al realizar la consulta " + error})

    finally:
        return flask.make_response(jsonify(ret), ret_code)


@class_bp.route('/api/lesson', methods=['GET'])
def getLesson(*args, **kwargs):

    ret = []
    ret_code = 400
    logger.info("Devolver el detalle de una leccion")

    try:
        results = Clase.get_levels_by_lesson(request.args.get('level'))
        if results is not None:
            for result in results:
                ret.append({"level": result.level})
            ret_code = 200
        else:
            logger.error("No hay más lecciones para %s" %
                         request.args.get('level'))

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error al recuperar la lección %s" % str(error))
        ret_code = 404
        ret.append({"Error": "Error al realizar la consulta " + error})

    finally:
        return flask.make_response(jsonify(ret), ret_code)


@class_bp.route('/api/clases', methods=['GET'])
def getClases(*args, **kwargs):
    '''
    Devuelve todas las clases de una lección

    Parameters:
        lesson (String): id de la lección

    Returns:
        json: objeto Clase

    Example {base_url}/api/class?lesson=1
    '''
    ret = []
    ret_code = 200
    logger.info("Devolver clases")
    try:
        results = Clase.get_all()
        for result in results:
            ret.append({"image": result.image,
                        "text": result.text,
                        "page": request.args.get('page'),
                        "total": str(len(results)),
                        "type": str(result.type)})
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error de acceso a la base de datos " + str(error))
        logger.error("Error de acceso a la base de datos " + str(error))
        ret_code = 404
        ret.append({"Error": "Error al realizar la consulta "})

    finally:
        return flask.make_response(jsonify(ret), ret_code)


@class_bp.route('/api/clase', methods=['GET'])
def getClase(*args, **kwargs):
    '''
    Devuelve las lecciones disponibles para un determinado nivel (curso)

    Parameters:
        level (String): Nivel de dificultad
        page (String):  Pagina de la lección

    Returns:
        json: objeto Clase

    Example {base_url}/api/clase?lesson=1&page=1&level=1
    '''
    ret = []
    ret_code = 400
    logger.info("Leeciones para el nivel %s , pagina %s" %
                (request.args.get('level'), request.args.get('page')))

    try:
        results = Clase.get_lesson(request.args.get('lesson'),
                                   request.args.get('level'),
                                   request.args.get('page'))

        if results is not None:
            ret.append({"image": results.image,
                        "text": results.text,
                        "page": request.args.get('page'),
                        "total": "1",
                        "type": str(results.type)})
            ret_code = 200
        else:
            logger.error("No hay más lecciones para %s" %
                         request.args.get('level'))

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error al recuperar la lección %s" % str(error))
        ret_code = 404
        ret.append({"Error": "Error al realizar la consulta " + error})

    finally:
        return flask.make_response(jsonify(ret), ret_code)


@class_bp.route('/api/question', methods=['GET'])
def getQuestions(*args, **kwargs):
    '''
    Devuelve las preguntas correspondintes a una determinada evaluación

    Parameters:
        level (String): Nivel de dificultad
        page (String):  Pagina de la lección
        lesson (String):Lección consultada

    Returns:
        json: objeto Evaluacion

    Example {base_url}/api/question?page=3&level=1&lesson=1
    '''
    ret = []
    ret_code = 400

    try:
        results = Evaluacion.get_evaluacion(request.args.get('level'),
                                            request.args.get('page'),
                                            request.args.get('lesson'))

        if results is not None:
            ret.append({
                "respuesta_1": results.pregunta1,
                "respuesta_2": results.pregunta2,
                "respuesta_3": results.pregunta3,
                "respuesta_4": results.pregunta4,
                "pregunta": results.text,
            })
            ret_code = 200
        else:
            logger.error("No hay preguntas para %s" %
                         request.args.get('level'))

    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error al recuperar la preguntas %s" % str(error))
        ret_code = 404
        ret.append({"Error": "Error al realizar la consulta " + error})

    finally:
        return flask.make_response(jsonify(ret), ret_code)


@class_bp.route('/api/answer', methods=['GET'])
def getAnswer(*args, **kwargs):
    '''
    Indica si la respuesta del usuario es correcta o no

    Parameters:
        level (String): Nivel de dificultad
        page (String):  Pagina de la lección
        lesson (String):Lección consultada
        answer (String):id de la respuesta

    Returns:
        Bool: True si la respuesta es correcta
              False en caso contrario

    Example {base_url}/api/answer?page=3&level=1&answer=1&answer=1
    '''

    ret = []
    ret_code = 200
    acerto = "false"
    try:
        results = Evaluacion.get_evaluacion(request.args.get('level'),
                                            request.args.get('page'),
                                            request.args.get('lesson'))
        if results is not None:
            if(str(results.respuesta) == request.args.get('answer')):
                acerto = "true"
            else:
                acerto = "false"
    except (Exception, psycopg2.DatabaseError) as error:
        logger.error("Error al recuperar la preguntas %s" % str(error))
        ret_code = 404
    finally:
        ret.append({"answer": acerto})

    return flask.make_response(jsonify(ret), ret_code)


@class_bp.errorhandler(404)
def error_404_handler(e):
    message = {
        'message': 'Resource Not Found ' + request.url,
        'status': 404
    }
    response = jsonify(message)
    response.status_code = 404
    return response
