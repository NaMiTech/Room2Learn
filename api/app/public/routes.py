from . import public_bp

from flask import Flask, jsonify
import logging
import datetime
import sys
import os

from flask import request, render_template, flash, redirect, url_for

logger = logging.getLogger(__name__)


@public_bp.route("/")
def index_page():
    app_name = os.environ["APP_NAME"]
    now = datetime.datetime.now()

    try:
        version = open("version", "r").read().strip()

    except Exception:
        version = 0
        logger.exception("No ha sido posible leer la version")

    return render_template("public/index.html", version=version,
                           app_name=app_name, year=now.year)


@public_bp.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404
