import os
# import datetime to use it to know the submitted time
import datetime

# import functions from credit to check whether the enterd card number valid or not
#from credit import get_total, get_length, check_amex, check_visa, check_master, turn_to_digits

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///contacts.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route('/')
@login_required
def home():
    return render_template('home.html')

# View contact list in another page
@app.route('/view_contacts')
@login_required
def view_contacts():
    return render_template('contacts.html')

# Log user in
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE name = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or rows[0]["password"] != request.form.get("password"):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# Log user out
@app.route("/logout")
def logout():
    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

# GEt the data and Validate them
@app.route('/contacts', methods=['GET', 'POST'])
@login_required
def get_contacts():
    # Get the user's ID
    user_id = session["user_id"]

    # Check wether the user reached using GET or POST
    if request.method == "GET":

        # Get the contacts using user_id
        contacts = db.execute("SELECT * FROM contacts WHERE user_id = ?", user_id)
        
        # Return it to the Js file to display it
        return jsonify([{
            'id': contact['id'],
            'first_name': contact['first_name'].strip(),
            'second_name': contact['second_name'] or 'None',
            'phone': contact['phone_number'],
            'email': contact['email'] or 'None',
            'category': contact['category']
        } for contact in contacts])
    else:
        #Get the entered data
        data = request.get_json()

        # Validation checks
        if not data.get('first_name').strip() or not data.get('phone').strip():
            return jsonify({"message": "First Name and Phone Number are required", "status": "error"}), 400
        # Check phone number length
        if len(data.get('phone').strip()) < 10:  
            return jsonify({"message": "Phone Number is too short", "status": "error"}), 400
        
        # Get the contacts that has same name or phone etc,
        existing_contact = db.execute(
            "SELECT * FROM contacts WHERE user_id = ? AND (first_name = ? AND second_name = ? OR phone_number = ? )",
            user_id,
            data['first_name'].strip(),
            data['second_name'].strip(),
            data['phone']
        )
        
        # Return an error message
        if existing_contact:
            return jsonify({"message": "Contact already exists", "status": "error"}), 400

        # The data is correct so insert it into the data base
        db.execute(
            "INSERT INTO contacts (user_id, first_name, second_name, phone_number, email, category) VALUES (?, ?, ?, ?, ?, ?)",
            user_id,
            data['first_name'].strip(),
            data['second_name'].strip(),
            data['phone'],
            data['email'],
            data['category']
        )

        # Return a Succeess message
        return jsonify({"message": "Contact added successfully", "status": "success"}), 201

# Activate the delete button    
@app.route('/contacts/<int:id>', methods=['DELETE'])
@login_required
def delete_contact(id):    
    # Get the user's Id using session
    user_id = session["user_id"]

    # Check if the contact belongs to the user
    contact = db.execute("SELECT * FROM contacts WHERE id = ? AND user_id = ?", id, user_id)
    if len(contact) != 1:
        # Return an Error message
        return jsonify({"message": "Contact not found or unauthorized"}), 404

    # Delete the contact
    db.execute("DELETE FROM contacts WHERE id = ?", id)
    
    # Return a success message
    return jsonify({"message": "Contact deleted"}), 200

# Register a new user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    
    # User reached via POST
    if request.method == "POST":
        # Assign data to variables
        name = request.form.get("username")
        password = request.form.get("password")
        cofirmation = request.form.get("confirmation")

        # Check if he has entered data or not
        if not name.strip():
            return apology("You must enter username", 400)
        elif not password:
            return apology("You must enter password", 400)
        elif password != cofirmation:
            return apology("They must be Identical", 400)
        
        # Query database for username
        names = db.execute(
            "SELECT * FROM users WHERE name = ?", name
        )
        if len(names) != 0:
            return apology("This username is already taken edit it", 403)
        
        # Insert data into the database
        db.execute("INSERT INTO users (name, password) VALUES(?, ?)", name, password)
        # Display a success message then redirect it to login  page
        flash("Successfully Registered!")
        return redirect("/login")

    # User reached via GET by clicking a link 
    else:
        return render_template("register.html")
