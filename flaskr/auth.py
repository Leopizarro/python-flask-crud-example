import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=["POST"])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        db = get_db()
        error = None

        if not username:
            error = 'Username is required'
        if not first_name:
            error = 'First name is required'
        if not last_name:
            error = 'Last name is required'
        if len(username) < 4:
            error = 'Username must be at least 4 characters long.'
        if len(password) < 6:
            error = 'The password must be at least 6 characters long.'
        if not password:
            error = 'Password is required'

        print('ERRORRRR->', error)

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (username, password, first_name, last_name) VALUES (?,?,?,?)", (username, generate_password_hash(password), first_name, last_name),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered"
            else:
                return {
                    "ok": True,
                    "message": f"User {username} created!"
                    }
        return error, 400
    return "Method not supported"
            

@bp.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM users WHERE username = ?', (username,)
        ).fetchone()

        print(user, username)

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            print('USER LOGGED IN!')
            session.clear()
            session['user_id'] = user['user_id']
            return {
                "ok": True,
                "message": f"user {user['username']} logged in!"
            }

        return {
            "ok": False,
            "message": error
        }

    return 'Method not supported'


@bp.route('/logout')
def logout():
    session.clear()
    return {
        "ok": True,
        "message": "USER LOGGED OUT"
    }


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view