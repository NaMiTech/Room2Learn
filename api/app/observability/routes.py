from . import observability_bp
from flask import Flask, jsonify
import logging
import flask
from app import create_app, db

logger = logging.getLogger(__name__)


@observability_bp.route('/healthy')
def status(*args, **kwargs):
    ret = []
    ret_code = 200
    ret.append({"subsystem": "api", "status": "ok"})

    try:
        res = "None"
        res = db.session.execute("SELECT true")
        ret.append({"subsytem": "bbdd", "status": "ok"})
    except Exception:
        logger.exception("Error al ejecutar el test de BBDD")
        # logger.critial(res)
        ret.append({"subsytem": "bbdd", "status": "ko"})
        ret_code = 500

    return flask.make_response(jsonify(ret), ret_code)


@observability_bp.route('/version')
def version(*args, **kwargs):
    ret = {}
    ret["version"] = "Error"
    ret_code = 500

    try:
        version = open("version", "r").read().strip()
        ret["version"] = version
        ret_code = 200
    except Exception:
        logger.exception("No ha sido posible leer la version")

    return flask.make_response(jsonify(ret), ret_code)
