from flask import Flask, render_template, redirect, url_for, reequest, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('project.html')

if __name__ == '__main__':
    app.run(debug=True)