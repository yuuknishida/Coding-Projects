from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)           # Initialize the Flask application
app.secret_key = "hello"            # Secret key for session management, replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'    # Database URI for SQLite
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False        # Disable modification tracking to save resources
app.permanent_session_lifetime = timedelta(minutes=5)       # Set the lifetime of the permanent session

db = SQLAlchemy(app)        # Initialize SQLAlchemy with the Flask app

# Define the users model, which represents the users table in the database
class users(db.Model):     
    _id = db.Column("id", db.Integer, primary_key=True)     # Primary key column
    name = db.Column(db.String(100))        # Name Column
    email = db.Column(db.String(100))       # Email Column

    def __init__(self, name, email):        
        self.name = name            # Initialize the name
        self.email = email          # Initialize the email



@app.route("/")             # Define the home route
def home():
    return render_template("index.html")        # Render the home page template

@app.route("/view")
def view():
    return render_template("view.html", values=users.query.all())


@app.route("/login", methods=["POST", "GET"])       # Define the login route
def login():
    if request.method == "POST":        # Handle form submission
        session.permanent = True        # Set the session to be permanent
        user = request.form["nm"]       # Get the username from the form
        session["user"] = user          # Store the username in the session

        found_user = users.query.filter_by(name=user).first()   # Check if the user exists in the database
        if found_user:
            session["email"] = found_user.email     # Store the user's email in the session if found
        
        else:
            usr = users(user, "")       # Create a new user with an empty email
            db.session.add(usr)         # Add the new user to the session
            db.session.commit()         # Commit the session to save the new user to the database

        flash("Login Successful")       # Flash a login successful message
        return redirect(url_for("user"))        # Redirect to the user page
    else:
        if "user" in session:               # If the user is already logged in
            flash("Already Logged In!")         # Flash a message indicating the user is already logged in
            return redirect(url_for("user"))        # Redirect to the user page
        
        return render_template("login.html")        # Render the login page template

@app.route("/user", methods=["POST", "GET"])        # Define the user route
def user():
    email = None                # Initialize email variable
    if "user" in session:           # Check if the user is logged in
        user = session["user"]          # Get the username from the session

        if request.method == "POST":        # Handle form submission for updating email
            email = request.form["email"]       # Get the email from the form
            session["email"] = email        #Update the session with the new email
            found_user = users.query.filter_by(name=user).first()       # Find the user in the database
            if found_user:
                found_user.email = email        # Update the user's email in the database
                db.session.commit()         # Commit the session to save changes to the database
                flash("Email was saved")        # Flash a message indicating the email was saved
        else:
            if "email" in session:          # If the email is already in the session
                email = session["email"]        # Get the email from the session

        return render_template("user.html", email=email)        # Render the user page template with the email
    else:
        flash("You are not logged in!")     # Flash a message indicating the user is not logged in
        return redirect(url_for("login"))       # Redirect to the login page
    
@app.route("/logout")       # Define the logout route
def logout():
    flash("You have been logged out!", "info")      # Flash a message indicating the user has been logged out
    session.pop("user", None)           # Remove the user from the session
    session.pop("email", None)          # Remove the email from the session
    return redirect(url_for("login"))       # Redirect to the login page

if __name__ == "__main__":
    with app.app_context():     # Ensure the database is created within the application context
        db.create_all()             # Create the database tables if they don't exist
    # Run the Flask application in debug mode
    app.run(debug=True)