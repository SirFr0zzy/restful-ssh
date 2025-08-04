from flask import jsonify, Blueprint, request

import app
from app import auth, require_args, sessions, get_client_ip
from sqlalchemy.orm import Session
from session import Session


handler = Blueprint('/exec', __name__)

@handler.route('/exec', methods=['POST'])
@require_args('session_id', 'command')
def action():

    client_ip = get_client_ip()
    engine = app.get_database_engine()

    command = request.args.get('command')
    session_id = int(request.args.get('session_id'))  # Convert to int since IDs from DB are integers

    with Session() as db:
        ip = get_owner_ip(db, session_id)
        if ip != client_ip:
            return jsonify({
                "error": "Session is outdated or invalid"
            }), 404


    client = sessions.get(session_id)
    if client is None:
        return jsonify({
            "error": "Couldn't find session"
        }), 404

    stdin, stdout, stderr = client.exec_command(command)

    return jsonify({
        "stdout": stdout.read().decode('utf-8'),
        "stderr": stderr.read().decode('utf-8')
    }), 200



def get_owner_ip(db, session_id: int) -> str | None:
    session_entry = db.query(Session).filter_by(id=session_id).first()
    if session_entry:
        return session_entry.owner_ip
    return None