import datetime
import json
import sqlite3
from flask import Blueprint, jsonify
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("project", __name__, url_prefix="/projects")

@bp.route("/", methods=['GET', 'POST'])
def index():
    db = get_db()
    """Return all the projects, most recent first"""
    if request.method == 'GET':
        try:
            data = db.execute(
                "SELECT project_id, project_title, project_description, created_at, updated_at, completed_at, completion_rate, u.user_id, u.username FROM projects p JOIN users u ON p.author_id = u.user_id ORDER BY created_at DESC"
            ).fetchall()
            print(data)
            projects = [dict(project_id=row[0], project_title=row[1], project_description=row[2], created_at=row[3], updated_at=row[4], completed_at=row[5], competion_rate=row[6], user_id=row[7], username=row[8]) for row in data]
            return projects
        except sqlite3.Error as e:
                return jsonify({"error": str(e)}), 500
    elif request.method == 'POST':
        try:
            project_title = request.form.get("project_title")
            project_description = request.form.get("project_description")
            created_at = request.form.get("created_at")
            author_id = request.form.get("author_id")
            completion_rate = request.form.get("completion_rate")
            project_categories = request.form.get("categories[]")
            if (project_title and project_description and created_at and author_id and completion_rate):
                newProject = db.execute("INSERT INTO projects (project_title, project_description, created_at, completion_rate, author_id) VALUES (?,?,?,?,?)", (project_title, project_description, created_at, completion_rate, author_id,))
                """ db.commit() """
                if project_categories:
                    categories_ids = json.loads(project_categories)
                    for category_id in categories_ids:
                        data = db.execute("SELECT * FROM categories c WHERE c.category_id=?", (category_id,)).fetchone()
                        if data:
                            db.execute("INSERT INTO project_category (project_id, category_id) VALUES (?,?)", (newProject.lastrowid, category_id))
                            print('CATEGORY INSERTED!->', category_id)
                        else:
                            return {
                                "ok": False,
                                "message": "Category for the project now found"
                            }, 404
                    db.commit()
                return jsonify({
                    "ok": True,
                    "message": "Project created successfully!"
                }), 200
            else:
                return jsonify({
                    "ok": False,
                    "message": "Please enter: project_title, project_description, created_at, completion_rate, author_id to create a project"
                }), 400
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "error": str(e)}), 500

@bp.route("/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def project(id):
    db = get_db()
    if request.method == 'GET':
        try:    
            project = db.execute("SELECT * FROM  projects p WHERE p.project_id=?", (id,)).fetchone()
            if project:
                return jsonify({"project_id": project[0], "project_title": project[1], "project_description": project[2],
                                "created_at": project[3], "updated_at": project[4], "completed_at": project[5],
                                "completion_rate": project[6]}), 200
            return jsonify({"ok": False, "message": "Project not found"}), 404
        except sqlite3.Error as e:
            return jsonify({"ok": False, "message": str(e)}), 500
    elif request.method == 'DELETE':
        try:
            project_to_delete = db.execute("SELECT * FROM projects p WHERE p.project_id=?", (id,)).fetchone()
            if project_to_delete:
                db.execute("DELETE FROM projects WHERE project_id = ?", (id,))
                db.commit()
                return jsonify({
                    "ok": True,
                    "message": f"Project with id: {id} has been deleted!"
                }), 200
            return jsonify({
                "ok": False,
                "message": f"Project with id {id} doesn't exists in the database"
            }), 404
        except sqlite3.Error as e:
            return jsonify({"ok": False, "message": str(e)}), 50
    elif request.method == "PUT":
        try:
            project_title = request.form.get("project_title")
            project_description = request.form.get("project_description")
            created_at = request.form.get("created_at")
            author_id = request.form.get("author_id")
            completion_rate = request.form.get("completion_rate")
            updated_at = datetime.datetime.now()
            if (project_title and project_description and created_at and author_id and completion_rate):
                project_to_update = db.execute("SELECT * FROM projects p WHERE p.project_id=?", (id,)).fetchone()
                if project_to_update:
                    db.execute("UPDATE projects SET project_title=?,  project_description=?,  created_at=?,  author_id=?,  completion_rate=?, updated_at=? WHERE project_id=?",
                                (project_title, project_description, created_at, author_id, completion_rate,updated_at, id))
                    db.commit()
                    return jsonify({
                        "ok": True,
                        "message": f'Project with id: {id} has been updated successfully!'
                    }), 200
                else:
                    return jsonify({
                        "ok": False,
                        "message": f"Project with id {id} not found"
                    }), 404
            else:
                return jsonify({
                    "ok": False,
                    "message": "Please enter all the information neccesary to update a project"
                }), 400
        except sqlite3.Error as e:
            return jsonify({"ok": False, "message": str(e)}), 500

@bp.route("/<int:id>/categories", methods=['GET'])
def get_project_categories(id):
    if request.method == 'GET':
        try:
            db = get_db()
            values = db.execute("SELECT * FROM project_category pc JOIN projects p ON pc.project_id=p.project_id JOIN categories c ON pc.category_id=c.category_id WHERE pc.project_id=?", (id,)).fetchall()
            list_comp_version = [{k: item[k] for k in item.keys()} for item in values]
            print(list_comp_version, id)
            return jsonify({
                "ok": True,
                "project_categories": list_comp_version
            })
        except sqlite3.Error as e:
            return jsonify({"ok": False, "message": str(e)}), 500

