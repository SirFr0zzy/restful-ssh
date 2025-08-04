from functools import wraps

from flask import Flask, request, jsonify
import os
import uuid

from flask.cli import load_dotenv
from sqlalchemy import create_engine, text

import routes

app = Flask(__name__)
load_dotenv()


def auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            auth_header = request.headers.get('Authorization')
            try:
                token = auth_header.split(' ')[1]
            except IndexError:
                pass

        if token is None:
            return jsonify({
                'error': 'Unauthorized'
            }), 401

        try:
            if token != os.getenv('API_TOKEN'):
                return jsonify({
                    'error': 'Unauthorized'
                }), 401
        except Exception as e:
            return jsonify({
                'error': 'Unauthorized'
            }), 401
        return f(*args, **kwargs)

    return decorated

def require_args(*required):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            missing = [arg for arg in required if arg not in request.args]
            if missing:
                return jsonify({
                    "message": f"Missing Parameter: {', '.join(missing)}"
                }), 400
            return f(*args, **kwargs)

        return wrapped

    return decorator

def get_client_ip():
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    return request.remote_addr


sessions = {}
session_id = str(uuid.uuid4())

def get_database_engine():
    engine = create_engine(f"mysql+pymysql://{os.getenv("DATABASE_USER")}:{os.getenv("DATABASE_PASS")}@{os.getenv("DATABASE_HOST")}:{os.getenv("DATABASE_PORT")}/restful", echo=True)
    return engine

def wipe_database():
    engine = get_database_engine()
    with engine.connect() as conn:
        conn.execute(text("DELETE FROM sessions;"))
        conn.commit()

if __name__ == '__main__':
    print(f"Agent Session: {session_id}")
    wipe_database()
    routes.register_routes(app=app)
    app.run(port=os.getenv('PORT'), host=os.getenv('HOST'))
