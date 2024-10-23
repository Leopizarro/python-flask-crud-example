

import sqlite3
from flask import Blueprint, jsonify, request

from flaskr.db import get_db


bp = Blueprint("activity_importance", __name__, url_prefix="/activity-importances")

@bp.route("/", methods=['GET','POST'])
def index():
    """Get all activity importances"""
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM activity_importances")
            activity_importances = [dict(activity_importance_id=row[0], activity_code=row[1], activity_description=row[2]) for row in data]
            return jsonify({
                "ok": True,
                "activity_importances": activity_importances
            })
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'POST':
        try:
            activity_code = request.form.get('activity_code')
            activity_description = request.form.get('activity_description')
            if (activity_code and activity_description):
                db.execute("INSERT INTO activity_importances (activity_code, activity_description) VALUES (?,?)", (activity_code, activity_description))
                db.commit()
                return jsonify({
                    "ok": True,
                    "message": f"New catgory created!: {activity_code}"
                })
            else:
                return jsonify({
                    "ok": False,
                    "message": "Please introduce the minimun information required to crreate an activity importance"
                }), 400
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500


@bp.route("/<int:id>", methods=['PUT', 'GET', 'DELETE'])
def activity_importance(id):
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM activity_importances ai WHERE ai.activity_importance_id=?", (id,)).fetchone()
            if (data):
                return jsonify({
                    "ok": True,
                    "activity_importance": {
                        "activity_importance_id": data[0],
                        "activity_code": data[1],
                        "activity_description": data[2]
                    }
                }), 200
            return jsonify({
                "ok": False,
                "message": 'Activity importance not found'
            }), 404
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'DELETE':
        try:
            data = db.execute("SELECT * FROM activity_importances ai WHERE ai.activity_importance_id=?", (id,)).fetchone()
            if data:
                db.execute("DELETE FROM activity_importances WHERE activity_importance_id=?", (id,))
                db.commit()
                return jsonify({
                "ok": True,
                "message": f'Activity importance with id {id} has been removed!'
            }), 200
            return jsonify({
                "ok": False,
                "message": 'Activity importance not found'
            }), 404
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'PUT':
        try:
            activity_code = request.form.get('activity_code')
            activity_description = request.form.get('activity_description')
            if activity_code and activity_description:
                data = db.execute("SELECT * FROM activity_importances ai WHERE ai.activity_importance_id=?", (id,)).fetchone()
                if data:
                    db.execute("UPDATE activity_importances SET activity_code=?, activity_description=? WHERE activity_importance_id=?", (activity_code, activity_description, id,))
                    db.commit()
                    return jsonify({
                    "ok": True,
                    "message": f'Activity importance with id {id} has been updated!'
                }), 200
                return jsonify({
                    "ok": False,
                    "message": 'Activity importance not found'
                }), 404
            else:
                return jsonify({
                    "ok": False,
                    "message": 'Please enter all the neccesary information to update an activity importance'
                }), 400
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
