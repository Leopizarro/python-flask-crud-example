

import sqlite3
from flask import Blueprint, jsonify, request

from flaskr.db import get_db


bp = Blueprint("category", __name__, url_prefix="/categories")

@bp.route("/", methods=['GET','POST'])
def index():
    """Get all categories"""
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM categories")
            categories = [dict(category_id=row[0], category_code=row[1], category_description=row[2]) for row in data]
            return jsonify({
                "ok": True,
                "categories": categories
            })
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'POST':
        try:
            category_code = request.form.get('category_code')
            category_description = request.form.get('category_description')
            if (category_code and category_description):
                db.execute("INSERT INTO categories (category_code, category_description) VALUES (?,?)", (category_code, category_description))
                db.commit()
                return jsonify({
                    "ok": True,
                    "message": f"New catgory created!: {category_code}"
                })
            else:
                return jsonify({
                    "ok": False,
                    "message": "Please introduce the minimun information required to crreate a project category"
                }), 400
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500


@bp.route("/<int:id>", methods=['PUT', 'GET', 'DELETE'])
def category(id):
    db = get_db()
    if request.method == 'GET':
        try:
            data = db.execute("SELECT * FROM categories c WHERE c.category_id=?", (id,)).fetchone()
            if (data):
                return jsonify({
                    "ok": True,
                    "category": {
                        "category_id": data[0],
                        "category_code": data[1],
                        "category_description": data[2]
                    }
                }), 200
            return jsonify({
                "ok": False,
                "message": 'Category not found'
            }), 404
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'DELETE':
        try:
            data = db.execute("SELECT * FROM categories c WHERE c.category_id=?", (id,)).fetchone()
            if data:
                db.execute("DELETE FROM categories WHERE category_id=?", (id,))
                db.commit()
                return jsonify({
                "ok": True,
                "message": f'Category with id {id} has been removed!'
            }), 200
            return jsonify({
                "ok": False,
                "message": 'Category not found'
            }), 404
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
    elif request.method == 'PUT':
        try:
            category_code = request.form.get('category_code')
            category_description = request.form.get('category_description')
            if category_code and category_description:
                data = db.execute("SELECT * FROM categories c WHERE c.category_id=?", (id,)).fetchone()
                if data:
                    db.execute("UPDATE categories SET category_code=?, category_description=? WHERE category_id=?", (category_code, category_description, id,))
                    db.commit()
                    return jsonify({
                    "ok": True,
                    "message": f'Category with id {id} has been updated!'
                }), 200
                return jsonify({
                    "ok": False,
                    "message": 'Category not found'
                }), 404
            else:
                return jsonify({
                    "ok": False,
                    "message": 'Please enter all the neccesary information to update a category'
                }), 400
        except sqlite3.Error as e:
            return jsonify({
                "ok": False,
                "message": str(e)
            }), 500
