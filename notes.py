from flask import Blueprint, render_template, request, redirect, flash, session
from cipher import AESCipher
import os
from datetime import datetime


notes = Blueprint("notes", __name__)

# Directory to store encrypted note files
NOTES_DIR = "encrypted_notes"
os.makedirs(NOTES_DIR, exist_ok=True)


@notes.route("/Dashboard")
def dashboard():
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to view your notes.", "warning")
        return redirect('/')

    user_dir = os.path.join(NOTES_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    try:
        notes = []
        for f in os.listdir(user_dir):
            if f.endswith('.txt'):
                file_path = os.path.join(user_dir, f)
                created = datetime.fromtimestamp(os.path.getctime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                modified = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
                notes.append({'filename': f, 'created': created, 'modified': modified})
        notes = sorted(notes, key=lambda x: x['modified'], reverse=True)
        return render_template('Dashboard.html', notes=notes)
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect('/')


# route for rendering to notewrite.html page
@notes.route('/noteWrite')
def noteWrite():
    return render_template('noteWrite.html')

@notes.route("/save_note", methods=["POST"])
def save_note():
    user_id = session.get('user_id')  # Retreive user_id
    aes_key = session.get('aes_key')  # Retrieve the password stored in the session

    if not user_id or not aes_key: # if anyone is empty, it means session is ended, login again
        flash("Please log in to save notes.", "warning")
        return redirect('/')

    cipher = AESCipher(aes_key)  # Initialize cipher with user's password
    old_title = request.form.get('old_title', '').strip()
    new_title = request.form['title'].strip()
    content = request.form['content'].strip()

    # Define the user's notes directory
    user_dir = os.path.join(NOTES_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    old_file_path = os.path.join(user_dir, f"{old_title}.txt") if old_title else None
    new_file_path = os.path.join(user_dir, f"{new_title}.txt")

    if new_title and content:
        try:
            # Encrypt the content
            encrypted_content = cipher.encrypt(content)

            # Rename the file if the title has changed
            if old_title and old_title != new_title:
                if old_file_path and os.path.exists(old_file_path):
                    os.rename(old_file_path, new_file_path)
                else:
                    flash("Original file not found, creating a new file.", "warning")

            # Save the encrypted content to the file
            with open(new_file_path, 'w') as file:
                file.write(encrypted_content)

            flash("Note saved successfully!", "success")
        except Exception as e:
            flash(f"An error occurred: {e}", "danger")
    else:
        flash("Please fill in all fields.", "warning")

    return redirect('/Dashboard')

@notes.route('/edit_note/<filename>')
def edit_note(filename):
    user_id = session.get('user_id')
    aes_key = session.get('aes_key')
    if not user_id or not aes_key:
        flash("Please log in to edit notes.", "warning")
        return redirect('/')

    cipher = AESCipher(aes_key)
    user_dir = os.path.join(NOTES_DIR, str(user_id))
    file_path = os.path.join(user_dir, filename)
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            encrypted_content = file.read()
        try:
            # Decrypt the content
            content = cipher.decrypt(encrypted_content)
            return render_template('noteWrite.html', title=filename.replace('.txt', ''), content=content)
        except Exception as e:
            flash(f"An error occurred while decrypting the note: {e}", "danger")
            return redirect('/Dashboard')
    else:
        flash("File not found.", "danger")
        return redirect('/Dashboard')
    

@notes.route('/delete_note/<filename>', methods=['GET'])
def delete_note(filename):
    user_id = session.get('user_id')
    if not user_id:
        flash("Please log in to delete notes.", "warning")
        return redirect('/')

    user_dir = os.path.join(NOTES_DIR, str(user_id))
    file_path = os.path.join(user_dir, filename)
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            flash("Note deleted successfully!", "success")
        except Exception as e:
            flash(f"An error occurred while deleting the note: {e}", "danger")
    else:
        flash("File not found.", "danger")

    return redirect('/Dashboard')