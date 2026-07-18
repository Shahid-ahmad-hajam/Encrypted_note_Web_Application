from flask import Flask
from auth import auth
from notes import notes

app = Flask(__name__)
app.secret_key = "your_secret_key"

app.register_blueprint(auth) # Flask copies all the routes stored in the blueprint into the application's 
# routing table. After registration, requests to /login_user are handled by the login_user() function.
app.register_blueprint(notes)

if __name__ == "__main__":
    app.run(debug=True)

# request is a Flask object that represents the current HTTP request sent by the browser to the server.

# In Flask, session is an object that represents user state and provides a dictionary-like interface 
# for storing session data.”