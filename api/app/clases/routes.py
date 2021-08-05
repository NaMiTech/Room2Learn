from . import class_bp
from flask import Flask, jsonify, request
import logging
import flask
from app import create_app, db


logger = logging.getLogger(__name__)


@class_bp.route('/api/class')
def getAllProducts(*args, **kwargs):
    ret = []
    ret_code = 200

    images = ['https://cdn2.unrealengine.com/Diesel%2Fproductv2%2Fzombie-army-4-dead-war%2Fhome%2FEGS_REBELLION_ZOMBIEARMY4_DELUXE_CAROUSEL_01-1920x1080-1124e35359380e698a6d5ef455e14b7fc9f64284.jpg',
              'https://media.istockphoto.com/photos/zombie-hand-holding-old-wooden-board-empty-space-for-text-or-draw-picture-id1166085591?k=6&m=1166085591&s=612x612&w=0&h=aYMvfmitwMSzJzqSszeUO_TOCBum7FMckCkB0OHIzHg=',
              'https://cdn02.nintendo-europe.com/media/images/10_share_images/games_15/nintendo_switch_4/H2x1_NSwitch_ZombieArmyTrilogy_image1280w.jpg']

    text = ['lalalalalallal',
            'lolololollololo',
            'lululululululu']

    page = int(request.args.get('page'))
    ret.append({"image": images[page],
                "text": text[page],
                "page": request.args.get('page'),
                "total": str(len(text)),
                "type": 'question'})

    return flask.make_response(jsonify(ret), ret_code)
