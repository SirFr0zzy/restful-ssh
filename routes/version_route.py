# File was created on 04.08.25 at 03:33 by Elias Lauterbach

from flask import jsonify, Blueprint
from app import auth, get_client_ip
import os

handler = Blueprint('/version', __name__)


@handler.route('/version', methods=['GET'])
def action():
    return {"version": os.getenv('VERSION')}, 200
