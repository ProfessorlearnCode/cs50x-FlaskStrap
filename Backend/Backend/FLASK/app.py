from flask import Flask, render_template, request, redirect, url_for, jsonify, session
from flask_socketio import join_room, leave_room, send, SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from flask_session import Session
from config import Config
from models import User
from database import db
import os
from datetime import datetime
import requests
from flask_migrate import Migrate
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Ensure instance folder for the SQLite file exists
basedir = os.path.abspath(os.path.dirname(__file__))
instance_dir = os.path.join(basedir, 'instance')
os.makedirs(instance_dir, exist_ok=True)
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(instance_dir, 'database.db')}"

CORS(app)



# Initialize Flask-Session and SQLAlchemy
Session(app)
db.init_app(app)
socketio = SocketIO(app, cors_allowed_origins="*")
migrate = Migrate(app, db)



# Ensure database tables are created
with app.app_context():
    db.create_all()

### ROUTES ###

@app.route('/')
def homepage():
    return render_template("homepage.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Step 1: Fetch the user from your local database
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            return jsonify({'success': False, 'error': "Could not log you in!"}), 400



        # Step 2: Authenticate with Strapi to get the JWT
        strapi_url = "http://localhost:3000"  # URL for Strapi API
        strapi_data = {
            "identifier": email,  # Strapi uses "identifier" for both email
            "password": password
        }

        try:
            strapi_response = requests.post(f"{strapi_url}/api/auth/local", json=strapi_data)

            if strapi_response.status_code == 200:
                strapi_response_data = strapi_response.json()
                strapi_token = strapi_response_data['jwt']  # Extract the JWT
            else:
                return jsonify({'success': False, 'error': "Strapi login failed!"}), 400

        except Exception as e:
            return jsonify({'success': False, 'error': "An error occurred during Strapi authentication!"}), 500

        # Step 3: Update session details
        session['user_id'] = user.id
        session['username'] = user.username
        session['strapi_token'] = strapi_token  # Store the JWT in the session


        return jsonify({'success': True, 'message': "Logging you in", 'strapi_token': strapi_token}), 200

    return render_template("login.html")



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        f_name = request.form.get('firstname')
        l_name = request.form.get('lastname')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        c_password = request.form.get('c_pass')
        role = request.form.get('role')  # e.g., 'viewer', 'author'

        if password != c_password:
            return jsonify({'success': False, 'error': "Passwords do not match!"}), 400

        hash_pass = generate_password_hash(password, method="scrypt")

        # Check if username or email already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'success': False, 'error': "Username already exists!"}), 400
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'error': "Email already registered!"}), 400

        # Create a new user and save to the local database
        new_user = User(
            firstname=f_name,
            lastname=l_name,
            username=username,
            email=email,
            password=hash_pass,
            role=role,
            city=request.form.get('city'),
        )


        # Registration Token used to enroll the
        strapi_token = "d8b23eef836c266894acef8b1cd911e933191c28d29c01f0e7d63a369ac151dffe33471a3368baae56a2692638a0054d0cdd275a18c7e9a19c6208fb0dfcad5749407f2b8cbf6a4899385636cbaa358fa07740b678be66a1557914fc103ff0d8a820042b03e9c138d7d18cb4a814e53aa0a1c340a10c670550b6f8a9ec8e3b8b"

        # Create user in Strapi
        user_data = {
            "username": username,
            "email": email,
            "password": password
        }

        headers = {
            "Authorization": f"Bearer {strapi_token}",
            "Content-Type": "application/json"
        }

        response = requests.post(f"http://localhost:3000/api/auth/local/register", json=user_data, headers=headers)
        db.session.add(new_user)
        db.session.commit()

        # Debugging
        if response.status_code == 201 or response.status_code == 200:  # User successfully created
            return jsonify({'success': True, 'message': "Registration successful! You can now log in."}), 200
        else:
            response_convert = response.json()
            response_message = response_convert["error"]["message"]
            print(f"Strapi response status: {response.status_code}")
            print(f"Strapi response body: {response.json()}")
            return jsonify({'success': False, 'error': f"{response_message}", 'details': response.json()}), 400

    return render_template("registeration.html")



@app.route('/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    session_user = session['user_id']
    current_user = User.query.get(session_user)
    print(current_user)

    if current_user:
        user_info = {
            'name': current_user.username,
            'email': current_user.email,
            'role': current_user.role
        }
        return render_template('userpanel.html', user=user_info)
    else:
        return redirect(url_for('login'))



@app.route('/change-password', methods=['POST'])
def change_password():
    user_id = session.get('user_id')  # Assuming user is logged in and session stores the user ID
    old_password = request.form['old_password']
    new_password = request.form['new_password']

    # Fetch the user from your local database
    user = User.query.get(user_id)

    if not user or not check_password_hash(user.password, old_password):
        return jsonify({'success': False, 'error': 'Old password is incorrect.'}), 400

    # Step 1: Update password locally
    hashed_new_password = generate_password_hash(new_password)
    user.password = hashed_new_password
    db.session.commit()


    # Strapi URL
    strapi_url = "http://localhost:3000/api/auth/change-password"

    # User's JWT (obtained during login)
    jwt_token = session['strapi_token']

    # New password details
    password_data = {
        "currentPassword": old_password,  # Current password to verify identity
        "password": new_password,  # New password to set
        "passwordConfirmation": new_password  # Confirm the new password
    }

    # Headers with Authorization
    headers = {
        "Authorization": f"Bearer {jwt_token}",
        "Content-Type": "application/json"
    }

    # Make the request to Strapi to change the password
    response = requests.post(strapi_url, json=password_data, headers=headers)

    # Check the response
    if response.status_code == 200:
        print("Password changed successfully:", response.json())
        return jsonify({'success': True, 'message': 'Password Changed successfully!'}), 200
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return jsonify({'success': False, 'error': 'Password change unsuccessful.'}), 400




@app.route('/delete-account', methods=['GET', 'POST'])
def delete_account():
    # Get user details from session
    user_id = session.get('user_id')  # Local DB user ID stored in session
    jwt_token = session.get('strapi_token')  # Strapi JWT token stored in session
    token = "3bc243987d97d31901d68a1261aaee409f72e91088ac720ad07d59a18946ee522c8f7c2492ee3950b41be54be788f901b9bd54ec16732e9bf427836ae89ed7053fce55aaaed2cea2a9c6e1c41924950409940bde8af091401958630a531c7c7511b234cca695033f488485f3789a4ff0ab6f316462741b668ec884f8521b99a5"

    # Step 1: Fetch the user from the local database
    user = User.query.get(user_id)

    if user:
        try:
            # Step 2: Delete the user from the local database
            db.session.delete(user)
            db.session.commit()
            print(f"User with ID {user_id} deleted from local database.")

            # Step 3: Fetch the user from Strapi using the email or username
            strapi_search_url = "http://localhost:3000/api/users"  # Adjust this to the appropriate endpoint
            sheaders = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }

            # Fetch user from Strapi using their email
            params = {
                'filters[email][$eq]': user.email  # Assuming email is used for identifying users
            }

            # Get the Strapi user details
            strapi_response = requests.get(strapi_search_url, headers=sheaders, params=params)

            if strapi_response.status_code != 200:
                return jsonify({'success': False, 'error': 'Failed to fetch user from Strapi'}), strapi_response.status_code

            strapi_user_data = strapi_response.json()

            # Assuming there's only one user with this email
            if not strapi_user_data:
                return jsonify({'success': False, 'error': 'User not found in Strapi'}), 404

            # Get Strapi user ID
            strapi_user_id = strapi_user_data[0]['id']

            # Step 4: Delete the user from Strapi
            delete_strapi_url = f"http://localhost:3000/api/users/{strapi_user_id}"
            delete_response = requests.delete(delete_strapi_url, headers=sheaders)

            # Step 5: Handle Strapi's response
            if delete_response.status_code == 200:
                # Clear the session after successful deletion
                session.clear()
                return jsonify({'success': True, 'message': 'Account deleted successfully from both local DB and Strapi!'}), 200
            else:
                return jsonify({'success': False, 'error': f"Failed to delete from Strapi: {delete_response.text}"}), delete_response.status_code

        except Exception as e:
            db.session.rollback()  # Rollback in case of failure
            print(e)
            return jsonify({'success': False, 'error': 'Error deleting account.'}), 500
    else:
        return jsonify({'success': False, 'error': 'User not found in local database.'}), 404






# GLOBAL VARIABLE DICTIONARY
content_dictionary = {
    'articles': []
}

def fetching_data():
    strapi_token = session.get('strapi_token')
    if not strapi_token:
        return redirect(url_for('login'))

    headers = {
        'Authorization': f'Bearer {strapi_token}'
    }
    response = requests.get("http://localhost:3000/api/articles/", headers=headers)
    if response.status_code == 200:
        fetched_data = response.json()
    else:
        return {"data": []}
    # Parsing the data to send to the webpage:
    global content_dictionary
    content_dictionary['articles'] = []

    # Loop through each article in the JSON data
    for article in fetched_data['data']:
        article_data = {  # Create a new dictionary for each article
            'ID': article['id'],
            'content': {
                'headline': article['headline'],
                'body': ""
            },
            'author': article['author'],
            'published': datetime.fromisoformat(article['publishedAt'][:-1])
        }

        # Concatenate body content
        for content_body in article['body']:
            article_data['content']['body'] += (content_body['children'][0]['text']) + '\n'

        # Add the article's dictionary to the main content dictionary
        content_dictionary['articles'].append(article_data)

    return content_dictionary


@app.route('/conpage')
def content():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    strapi_token = session.get('strapi_token')
    if not strapi_token:
        return redirect(url_for('login'))

    content_dictionary = fetching_data()

    # Return to render the template with the lists
    return render_template("content.html", content_dictionary=content_dictionary)

@app.route('/article/<int:article_id>')
def article_detail(article_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))

    print(f"Requested article ID: {article_id}")  # Debug line

    content_dictionary = fetching_data()

    # Initialize article as None
    article = None

    # Loop through articles and find the matching one
    for art in content_dictionary['articles']:
        if art['ID'] == article_id:
            article = art
            break  # Exit the loop once the article is found

    print(f"Found article: {article}")  # Debug line

    if article:
        return render_template('article_page.html', article=article)
    else:
        return "Article not found", 404





@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))




@app.route('/chatroom')
def chatroom():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template("chatroom.html")


### SOCKET.IO EVENTS ###

@socketio.on('join')
def handle_join(data):
    username = session.get('username', 'Guest')
    room = data['room']
    join_room(room)
    send({'username': username, 'message': f"{username} has joined the room."}, to=room)

@socketio.on('message')
def handle_message(data):
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    room = data['room']
    if user:
        send({'username': user.username, 'message': data['message']}, to=room)
    else:
        send({'message': "An unknown user sent a message."}, to=room)

@socketio.on('leave')
def handle_leave(data):
    username = session.get('username', 'Guest')
    room = data['room']
    leave_room(room)
    send({'username': username, 'message': f"{username} has left the room."}, to=room)

if __name__ == '__main__':
    socketio.run(app, host='127.0.0.1', port=5000, debug=True)
