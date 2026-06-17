# 🚀 Quick Note Application

A full-stack note-taking application built using **React, Flask, SQLite, JWT Authentication, and REST APIs**.

The project demonstrates frontend-backend communication, CRUD operations, authentication, authorization, database integration, and full-stack web development fundamentals.

---

# 📌 Project Overview

Quick Note Application allows users to:

* Register a new account
* Login securely
* Create notes
* View notes
* Update notes
* Delete notes
* Store notes in a SQLite database
* Secure routes using JWT Authentication
* Prevent unauthorized access to notes

---

# ✨ Features

## Authentication

* User Registration
* User Login
* Password Hashing using bcrypt
* JWT Authentication
* Protected API Routes
* Logout Functionality
* Invalid Email Detection
* Account Lock after 3 Wrong Password Attempts
* Automatic Unlock after 5 Minutes

## Notes Management

* Create Notes
* Read Notes
* Update Notes
* Delete Notes
* Real-time Notes Refresh
* Date & Time Tracking

## User Interface

* Modern UI
* Gradient Background
* Glassmorphism Design
* Responsive Layout
* Smooth Animations
* Notes Counter
* Edit Notes
* Delete Notes

---

# 🛠 Tech Stack

## Frontend

* React (Vite)
* Axios
* CSS3

## Backend

* Python
* Flask
* Flask-CORS
* Flask-JWT-Extended
* bcrypt

## Database

* SQLite

---

# 📂 Project Structure

```text
Quick Note Application/

├── backend/
│   ├── app.py
│   ├── notes.db
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── Login.jsx
│   │   ├── Register.jsx
│   │   ├── App.css
│   │   └── main.jsx
│   │
│   ├── .env
│   ├── package.json
│   └── vite.config.js
│
├── README.md
└── .gitignore
```

---

# 🗄 Database Schema

## Notes Table

```sql
CREATE TABLE notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Users Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    failed_attempts INTEGER DEFAULT 0,
    lock_until TEXT
);
```

---

# 🔐 Authentication Flow

```text
User Registration
        ↓
Password Hashed (bcrypt)
        ↓
Stored in SQLite
        ↓
User Login
        ↓
JWT Token Generated
        ↓
Token Stored in Local Storage
        ↓
Access Protected Notes Routes
```

---

# 🔄 API Endpoints

## Authentication

### Register User

```http
POST /register
```

Request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "message": "Registration successful"
}
```

---

### Login User

```http
POST /login
```

Request:

```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Response:

```json
{
  "message": "Login successful",
  "token": "JWT_TOKEN"
}
```

---

## Notes APIs

### Get All Notes

```http
GET /notes
```

Authorization Required:

```text
Bearer Token
```

---

### Create Note

```http
POST /notes
```

Request:

```json
{
  "content": "My Note"
}
```

---

### Update Note

```http
PUT /notes/:id
```

Request:

```json
{
  "content": "Updated Note"
}
```

---

### Delete Note

```http
DELETE /notes/:id
```

---

# 🔒 Security Features

## Password Hashing

Passwords are hashed using:

```text
bcrypt
```

before being stored in the database.

---

## JWT Authentication

Protected routes require:

```text
Authorization: Bearer <token>
```

---

## Account Lock Protection

After:

```text
3 failed login attempts
```

the account is locked for:

```text
5 minutes
```

to prevent brute-force attacks.

---

# ⚙ Environment Variables

## Backend (.env)

```env
JWT_SECRET_KEY=your_secret_key
```

---

## Frontend (.env)

```env
VITE_API_URL=http://127.0.0.1:5000
```

For deployment:

```env
VITE_API_URL=https://your-backend.onrender.com
```

---

# 🚀 Installation

## Clone Repository

```bash
git clone <repository-url>
```

---

## Backend Setup

Navigate to backend:

```bash
cd backend
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run backend:

```bash
python app.py
```

Backend runs on:

```text
http://127.0.0.1:5000
```

---

## Frontend Setup

Navigate to frontend:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Run frontend:

```bash
npm run dev
```

Frontend runs on:

```text
http://localhost:5173
```

---

# 🌐 Deployment

## Frontend

Deploy on:

* Vercel

## Backend

Deploy on:

* Render

---

# 📈 Project Status

| Module              | Status     |
| ------------------- | ---------- |
| Flask Backend       | ✅ Complete |
| SQLite Database     | ✅ Complete |
| Notes CRUD          | ✅ Complete |
| Authentication      | ✅ Complete |
| JWT Authorization   | ✅ Complete |
| Account Lock System | ✅ Complete |
| React Frontend      | ✅ Complete |
| Deployment Ready    | ✅ Complete |

---

# 🎯 Learning Outcomes

This project demonstrates:

* Full Stack Development
* REST API Development
* React State Management
* JWT Authentication
* Password Hashing
* Database Operations
* CRUD Operations
* Frontend & Backend Integration
* Environment Variables
* Deployment Workflow

---

# 👨‍💻 Author

**SOHAM CHHUALSINGH**

B.Tech Computer Science Student

Full Stack Development | React | Flask | Python | SQLite
