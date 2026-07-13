from flask import Blueprint, render_template, request, redirect, flash, session
from cursor import cursor, db

auth = Blueprint("auth", __name__)

@auth.route("/")
def login_page():
    return render_template("loginpage.html")

@auth.route("/login_user", methods=["POST"])
def login_user():
    email = request.form['email']
    password = request.form['password']

    if not (email and password): # if one is empty
        flash("Please fill in all fields.", "warning") # if user pressed login button without entering detials
        return redirect('/') # back to defualt route

    try:
        query = "SELECT id, Name FROM miniprojectregister WHERE Email = %s AND Password = %s"
        cursor.execute(query, (email, password)) # To execute the above query 
        user = cursor.fetchone() # Returns a tuple of user_id & user_name e.g, (8,'Shahid6')

        if user:
            session['user_id'] = user[0]  # Store user's ID in session
            session['user_name'] = user[1]  # Store user's name in session
            session['aes_key'] = password  # Store password to use for AES encryption
            flash("Login successful!", "success")
            return redirect('/Dashboard')
        else:
            flash("Invalid email or password.", "danger")
            return redirect('/')
    except Exception as e:
        flash(f"An error occurred: {e}", "danger")
        return redirect('/')
    

# register route from login page
@auth.route('/register')
def register_page():
    return render_template('registerpage.html')

@auth.route('/register', methods=['POST'])
def register_user():
    name = request.form['name']
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirmPassword']

    if not (name and email and password and confirm_password):
        flash("All fields are required!", "warning")
        return redirect('/register')

    if password != confirm_password:
        flash("Passwords do not match!", "danger")
        return redirect('/register')

    try:
        query = "INSERT INTO miniprojectregister (Name, Email, Password) VALUES (%s, %s, %s)"
        cursor.execute(query, (name, email, password))
        db.commit()
        flash("Registration successful! You can now log in.", "success")
        return redirect('/')
    except Exception as e:
        db.rollback()
        flash(f"An error occurred: {e}", "danger")
        return redirect('/')


@auth.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_name', None)
    session.pop('user_password', None)

    flash("You have been logged out.", "info")
    return redirect('/')