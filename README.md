# Encrypted Notes Web Application

## Overview

This is a Flask-based web application for securely creating, editing, and managing personal notes. Each note is encrypted before being saved to disk, so the content remains private and protected.

Users can:

- register and log in
- create, edit, and delete notes
- view note metadata such as creation and modification time
- store notes in encrypted files under their own user folder

## Features

- User authentication with MySQL
- AES encryption for note content
- Dashboard to manage notes
- Session-based login flow
- Flash messages for feedback
- Modular Flask structure using blueprints

## Tech Stack

- Backend: Python, Flask
- Database: MySQL
- Frontend: HTML, CSS, Jinja2 templates
- Encryption: AES (CBC mode) using pycryptodome

## Project Structure

```text
Encrypted Note Application Mini Project 5th Sem/
├── app.py                 # Main Flask app entry point
├── auth.py                # Authentication routes (login, register, logout)
├── notes.py               # Note management routes (dashboard, save, edit, delete)
├── cipher.py              # AES encryption and decryption logic
├── cursor.py              # MySQL database connection
├── templates/             # HTML templates
├── static/                # CSS and static assets
├── encrypted_notes/       # Folder where encrypted note files are stored
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

## Installation

1. Clone or open the project folder.
2. Create a virtual environment:
   ```bash
   python -m venv venv
   ```
3. Activate the virtual environment:
   ```bash
   venv\Scripts\activate
   ```
4. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Database Setup

Create a MySQL database and table before running the app.

```sql
CREATE DATABASE shahid1;

USE shahid1;

CREATE TABLE miniprojectregister (
    id INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100),
    Email VARCHAR(100) UNIQUE,
    Password VARCHAR(100)
);
```

Update your MySQL credentials in [cursor.py](cursor.py) if needed:

```python
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="YourPassword",
    database="shahid1"
)
```

## Running the Application

Start the Flask server:

```bash
python app.py
```

Then open:

```text
http://127.0.0.1:5000/
```

## Encryption Details

- Encryption algorithm: AES in CBC mode
- Key generation: SHA-256 hash of the user's password, truncated to 16 bytes
- Padding: PKCS7-style padding
- IV: randomly generated for each encryption

## Notes

The application now uses a modular structure where authentication and note operations are handled in separate modules for better organization and maintainability.
