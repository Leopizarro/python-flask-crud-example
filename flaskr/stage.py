

import sqlite3
from flask import Blueprint, jsonify, request

from flaskr.db import get_db


bp = Blueprint("stage", __name__, url_prefix="/stages")

@bp.route("/", methods=['GET','POST'])
def index():
    """Get all stages"""
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM stages")
            stages = [dict(stage_id=row[0], stage_code=row[1], stage_description=row[2]) for row in data]
            return jsonify({
                "ok": True,
                "stages": stages
            })
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'POST':
        try:
            stage_code = request.form.get('stage_code')
            stage_description = request.form.get('stage_description')
            if (stage_code and stage_description):
                db.execute("INSERT INTO stages (stage_code, stage_description) VALUES (?,?)", (stage_code, stage_description))
                db.commit()
                return jsonify({
                    "ok": True,
                    "message": f"New stage created!: {stage_code}"
                })
            else:
                return jsonify({
                    "ok": False,
                    "message": "Please fill the minimun information required to crreate a stage"
                }), 400
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500


@bp.route("/<int:id>", methods=['PUT', 'GET', 'DELETE'])
def stage(id):
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM stages s WHERE s.stage_id=?", (id,)).fetchone()
            if (data):
                return jsonify({
                    "ok": True,
                    "stage": {
                        "stage_id": data[0],
                        "stage_code": data[1],
                        "stage_description": data[2]
                    }
                }), 200
            return jsonify({
                "ok": False,
                "message": 'Stage not found'
            }), 404
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'DELETE':
        try:
            data = db.execute("SELECT * FROM stages s WHERE s.stage_id=?", (id,)).fetchone()
            if data:
                db.execute("DELETE FROM stages WHERE stage_id=?", (id,))
                db.commit()
                return jsonify({
                "ok": True,
                "message": f'Stage with id {id} has been removed!'
            }), 200
            return jsonify({
                "ok": False,
                "message": 'Stage not found'
            }), 404
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'PUT':
        try:
            stage_code = request.form.get('stage_code')
            stage_description = request.form.get('stage_description')
            if stage_code and stage_description:
                data = db.execute("SELECT * FROM stages s WHERE s.stage_id=?", (id,)).fetchone()
                if data:
                    db.execute("UPDATE stages SET stage_code=?, stage_description=? WHERE stage_id=?", (stage_code, stage_description, id,))
                    db.commit()
                    return jsonify({
                    "ok": True,
                    "message": f'Stage with id {id} has been updated!'
                }), 200
                return jsonify({
                    "ok": False,
                    "message": 'Stage not found'
                }), 404
            else:
                return jsonify({
                    "ok": False,
                    "message": 'Please enter all the neccesary information to update a stage'
                }), 400
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
