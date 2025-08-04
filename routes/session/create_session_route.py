# File was created on 04.08.25 at 03:15 by Elias Lauterbach
from io import StringIO
from urllib.parse import unquote

from flask import jsonify, Blueprint, request
from sqlalchemy.orm import sessionmaker

import app
from app import auth, require_args
import os
from session import Session
import paramiko

handler = Blueprint('/session', __name__)


@handler.route('/session', methods=['POST'])
def action():
    json = request.get_json()
    host = json['host']
    port = json['port']
    user = json['username']
    password = json.get('password')
    ssh_key = json.get('ssh_key')
    client_ip = app.get_client_ip()

    agent_id = app.session_id

    print(f"Agent Session: {agent_id}")


    engine = app.get_database_engine()
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    _session = Session(
        host = host,
        port = port,
        user = user,
        password = password,
        private_key = ssh_key,
        owner_ip=client_ip,
        agent_session_uuid=agent_id
    )

    session.add(_session)
    session.commit()

    session_id = _session.id

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # unsichere Hosts automatisch akzeptieren

    if ssh_key:
        client.connect(hostname=host, port=port, username=user, pkey=parse_ssh_key(ssh_key))
    else:
        client.connect(hostname=host, port=port, username=user, password=password)

    app.sessions[session_id] = client

    return jsonify({
        "session_id": session_id
    }), 200


def parse_ssh_key(ssh_key_raw: str) -> paramiko.PKey:
    # Falls escaped übergeben (z. B. \n als 2 Zeichen), hier ersetzen:
    fixed_key = ssh_key_raw.replace("\\n", "\n")

    key_file = StringIO(fixed_key)
    return paramiko.RSAKey.from_private_key(key_file)
