



import sqlite3
from flask import Blueprint, jsonify

from flaskr.db import get_db


bp = Blueprint("user", __name__, url_prefix='/users')

@bp.route("/")
def index():
    """Return all users"""
    try:
        db = get_db()
        data = db.execute("SELECT user_id, username, first_name, last_name from users").fetchall()
        users = [dict(user_id=row[0], username=row[1], first_name=row[2], last_name=row[3]) for row in data]
        return jsonify(users), 200
    except sqlite3.Error as e:
            return jsonify({"error": str(e)}), 500

@bp.route("/<int:id>")
def get_user_by_id(id):
    try:
        db = get_db()
        data = db.execute("SELECT user_id, username, first_name, last_name from users u WHERE u.user_id=?", (id,)).fetchone()
        if data:
            user = {
             "user_id":data[0], "username":data[1], "first_name":data[2], "last_name":data[3]
            }
            return jsonify({
                "ok": True,
                "user": user
            }), 200
        else:
            return jsonify({
                "ok": False,
                "message": "User not found"
            }), 404
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
