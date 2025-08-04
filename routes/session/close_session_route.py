# File was created on 04.08.25 at 03:15 by Elias Lauterbach
from io import StringIO
from urllib.parse import unquote

from flask import jsonify, Blueprint, request
from sqlalchemy.orm import sessionmaker

from app import auth, require_args
import os
from session import Session
import paramiko

handler = Blueprint('/session', __name__)


@handler.route('/session', methods=['POST'])
@require_args('session_id')
def action():
    engine = app.get_database_engine()
    db_session = Session(engine)
    session = db_session.query(Session).filter_by(id=request.args.get('session_id')).first()

    if session:
        db_session.delete(session)
        db_session.commit()

    ssh_session = app.sessions.get(request.args.get('session_id'))
    ssh_session.close()
    app.sessions.remove(session)

    return {"message": "Session closed"}, 200
