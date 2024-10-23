import sqlite3
from flask import Blueprint, jsonify, request
from datetime import datetime


from flaskr.db import get_db

bp = Blueprint("milestone", __name__, url_prefix="/milestones")

@bp.route("/", methods=['GET', 'POST'])
def index ():
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM milestones")
            milestones = [dict(
                milestone_id=row[0],
                project_id=row[1],
                activity_importance_id=row[2],
                stage_id=row[3],
                milestone_title=row[4],
                milestone_description=row[5],
                created_at=row[6],
                updated_at=row[7],
                completed_at=row[8],
                milestone_observation=row[9],
                ) for row in data]
            return jsonify({
                "ok": True,
                "milestones": milestones,
            }), 200
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'POST':
        try:
            project_id=request.form.get('project_id')
            activity_importance_id=request.form.get('activity_importance_id')
            stage_id=request.form.get('stage_id')
            milestone_title=request.form.get('milestone_title')
            milestone_description=request.form.get('milestone_description')
            created_at=request.form.get('created_at')
            completed_at=request.form.get('completed_at')
            milestone_observation=request.form.get('milestone_observation')
            if (project_id and activity_importance_id and stage_id and milestone_title and milestone_description and milestone_observation):
                project_in_db = db.execute("SELECT * FROM projects p WHERE p.project_id=?", (project_id,)).fetchone()
                stage_in_db = db.execute("SELECT * FROM stages s WHERE s.stage_id=?", (stage_id,)).fetchone()
                activity_imp_in_db = db.execute("SELECT * FROM activity_importances ai WHERE ai.activity_importance_id=?", (activity_importance_id,)).fetchone()
                if project_in_db is None or stage_in_db is None or activity_imp_in_db is None:
                    return {
                        "ok": False,
                        "message": "Make sure that the project, stage, and the importance of the activity exists in the database"
                    }, 400

                if created_at is None:
                    created_at = datetime.now()
                updated_at = datetime.now()
                print(project_id, activity_importance_id, stage_id, milestone_title, milestone_description, milestone_observation, created_at, updated_at, completed_at)
                db.execute("INSERT INTO milestones (project_id, activity_importance_id, stage_id, milestone_title, milestone_description, milestone_observation, created_at, updated_at, completed_at) VALUES (?,?,?,?,?,?,?,?,?)",
                           (project_id, activity_importance_id, stage_id, milestone_title, milestone_description, milestone_observation, created_at, updated_at, completed_at))
                db.commit()
                return jsonify({
                    "ok": True,
                    "message": f"New milestone created!: {milestone_title}"
                }), 200
            else:
                return jsonify({
                    "ok": False,
                    "message": "Please fill the minimun information required to crreate a milestone"
                }), 400

        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500

@bp.route('/<int:id>', methods=['PUT', 'GET', 'DELETE'])
def milestone(id):
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM milestones m WHERE m.milestone_id=?", (id,)).fetchone()
            print(data, id)
            if data:
                return {
                    "ok": True,
                    "milestone": {
                        "project_id":            data[0],
                        "activity_importance_id":data[1],
                        "stage_id":              data[2],
                        "milestone_title":       data[3],
                        "milestone_description": data[4],
                        "created_at":            data[5],
                        "completed_at":          data[6],
                        "milestone_observation": data[7],
                    } 
                }
            return {
                "ok": False,
                "message": "Milestone not found"
            }, 404
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'DELETE':
        try:
            milestone_to_delete = db.execute("SELECT * FROM milestones m WHERE m.milestone_id=?", (id,)).fetchone()
            if milestone_to_delete:
                db.execute("DELETE FROM milestones WHERE milestone_id=?", (id,))
                db.commit()
                return {
                    "ok": True,
                    "message": f"Milestone with id: {id} has been deleted!" 
                }, 200
            return {
                "ok": False,
                "message": "Milestone not found"
            }, 404

        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'PUT':
        try:
            project_id=request.form.get('project_id')
            activity_importance_id=request.form.get('activity_importance_id')
            stage_id=request.form.get('stage_id')
            milestone_title=request.form.get('milestone_title')
            milestone_description=request.form.get('milestone_description')
            created_at=request.form.get('created_at')
            completed_at=request.form.get('completed_at')
            milestone_observation=request.form.get('milestone_observation')
            if (project_id and activity_importance_id and stage_id and milestone_title and milestone_description and milestone_observation):
                milestone_to_update = db.execute("SELECT * FROM milestones m WHERE m.milestone_id=?", (id,))
                if milestone_to_update:
                    updated_at = datetime.now()
                    db.execute("UPDATE milestones SET project_id=?, activity_importance_id=?, stage_id=?, milestone_title=?, milestone_description=?, milestone_observation=?, created_at=?, updated_at=?, completed_at=? WHERE m.milestone_id=?",
                               (project_id, activity_importance_id, stage_id, milestone_title, milestone_description, milestone_observation, created_at, updated_at, completed_at, id,))
                    db.commit()
                    return {
                        "ok": True,
                        "message": f"milestone with id: {id} has been deleted successfully!"
                    }, 200
                return {
                    "ok":False,
                    "message": "Milestone not found"
                }, 404
            return {
                "ok": False,
                "message": "Please add the minimun info required to update a milestone"
            }
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500

