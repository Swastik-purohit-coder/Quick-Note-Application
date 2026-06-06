from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import bcrypt
from datetime import datetime, timedelta
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required
)
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")

jwt = JWTManager(app)

DATABASE = "notes.db"


# Create table automatically
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            failed_attempts INTEGER DEFAULT 0,
            lock_until TEXT
        )
    """)

    conn.commit()
    conn.close()


# Home Route
@app.route("/")
def home():
    return "Flask Backend Running Successfully!"


# Create Note
@app.route("/notes", methods=["POST"])
@jwt_required()
def save_note():

    data = request.get_json()

    content = data.get("content")

    if not content:
        return jsonify({
            "error": "Content is required"
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO notes (content)
        VALUES (?)
        """,
        (content,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Note Saved Successfully"
    })


# Get All Notes
@app.route("/notes", methods=["GET"])
@jwt_required()
def get_notes():

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, content, created_at
        FROM notes
        ORDER BY id DESC
    """)

    notes = cursor.fetchall()

    conn.close()

    result = []

    for note in notes:
        result.append({
            "id": note[0],
            "content": note[1],
            "created_at": note[2]
        })

    return jsonify(result)


# Update Note
@app.route("/notes/<int:id>", methods=["PUT"])
@jwt_required()
def update_note(id):

    data = request.get_json()

    content = data.get("content")

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE notes
        SET content = ?
        WHERE id = ?
        """,
        (content, id)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Note Updated Successfully"
    })


# Delete Note
@app.route("/notes/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_note(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM notes
        WHERE id = ?
        """,
        (id,)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Note Deleted Successfully"
    })



@app.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({
            "message": "Email and password required"
        }), 400

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:
        conn.close()

        return jsonify({
            "message": "Email already exists"
        }), 400

    hashed_password = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()

    cursor.execute(
        """
        INSERT INTO users (email, password)
        VALUES (?, ?)
        """,
        (email, hashed_password)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "message": "Registration successful"
    })


@app.route("/login", methods=["POST"])
def login():

    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE email = ?",
        (email,)
    )

    user = cursor.fetchone()

    # Email not found
    if not user:
        conn.close()

        return jsonify({
            "message": "Email does not exist"
        }), 404

    # Check lock
    if user["lock_until"]:

        lock_time = datetime.fromisoformat(
            user["lock_until"]
        )

        if datetime.now() < lock_time:

            conn.close()

            return jsonify({
                "message": "Account locked for 5 minutes"
            }), 403

    # Wrong password
    if not bcrypt.checkpw(
        password.encode(),
        user["password"].encode()
    ):

        attempts = user["failed_attempts"] + 1

        # Lock account after 3 attempts
        if attempts >= 3:

            lock_until = (
                datetime.now()
                + timedelta(minutes=5)
            )

            cursor.execute(
                """
                UPDATE users
                SET failed_attempts=?,
                    lock_until=?
                WHERE email=?
                """,
                (
                    attempts,
                    lock_until.isoformat(),
                    email
                )
            )

            conn.commit()
            conn.close()

            return jsonify({
                "message": "Account locked for 5 minutes"
            }), 403

        cursor.execute(
            """
            UPDATE users
            SET failed_attempts=?
            WHERE email=?
            """,
            (
                attempts,
                email
            )
        )

        conn.commit()
        conn.close()

        return jsonify({
            "message": f"Wrong password ({attempts}/3)"
        }), 401

    # Successful login
    cursor.execute(
        """
        UPDATE users
        SET failed_attempts=0,
            lock_until=NULL
        WHERE email=?
        """,
        (email,)
    )

    conn.commit()
    conn.close()

    token = create_access_token(
        identity=email
    )

    return jsonify({
        "message": "Login successful",
        "token": token
    })


if __name__ == "__main__":
    init_db()
    app.run(debug=True)