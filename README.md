# 🎓 CS50x Final Project: FlaskStrap - Web Application with Flask and Strapi

🔗 **Video Demo:** [Watch here](https://youtu.be/WWoUpCO7WGg)

---

## 📖 Description

This project is a full-stack web application built as the **final project for Harvard’s CS50x** course. It combines a Python-based Flask backend with a powerful headless CMS using Strapi. The application enables:

- 🧑 User registration and login
- 📰 Content creation and management
- 💬 Real-time chat between users
- 🔐 Role-based access control

It integrates modern technologies such as **Flask-SocketIO** for real-time features and **SQLite** for lightweight database needs. Strapi serves as the backend CMS to manage articles, content types, and API access.

---

## ✨ Features

- 🔐 User authentication and secure registration
- 👥 Role-based access (viewer, author)
- 📝 Content creation and fetching via Strapi
- 💬 Real-time chat using WebSockets (Socket.IO)
- 🧑‍💻 User profile management
- 📡 API-driven dynamic content loading

---

## 🛠️ Technologies Used

| Backend            | Frontend         | CMS         |
|--------------------|------------------|-------------|
| Flask (Python)     | HTML/CSS         | Strapi      |
| Flask-SocketIO     | Bootstrap        | SQLite DB   |
| Werkzeug (security)| JavaScript       | Node.js     |

---

## 🧰 Installation and Setup

### 🔗 Prerequisites

Make sure the following are installed:

- [Node.js](https://nodejs.org/) (v18.x - v20.x)
- [Yarn](https://classic.yarnpkg.com/en/docs/install)
- [Python 3.8+](https://www.python.org/downloads/)
- [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/)

---

### 🐍 Set Up the Flask Backend

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate       # On Windows use `venv\Scripts\activate`

# Install required packages
pip install -r requirements.txt
````

---

### 🚀 Set Up the Strapi CMS

```bash
# Navigate to Strapi directory
cd Strapi

# Install dependencies
yarn install

# Start Strapi in development mode
yarn develop
```

* Access the Strapi admin at: `http://localhost:1337/admin`
* Default API access at: `http://localhost:1337/api/...`

---

### 🔥 Run the Flask Application

```bash
# In a separate terminal
cd path/to/your/flask-app

# Start the Flask server
flask run
```

* App will run at: `http://127.0.0.1:5000`

---

## 🧩 Strapi Setup Guide (Quick Overview)

1. **Install Strapi with Quickstart:**

   ```bash
   npx create-strapi-app my-project --quickstart
   cd my-project
   yarn develop
   ```

2. **Configure Your Database (Optional)**
   Edit `config/database.js` for PostgreSQL, MongoDB, etc.

3. **Create Content Types**
   Use Strapi's Content Type Builder to define schemas like `Articles`, `Users`, etc.

4. **Set Permissions**
   Go to **Settings → Roles** and configure access levels for `public`, `authenticated`, etc.

5. **Test Your APIs**

   * With tools like **Postman**
   * Via built-in API Explorer at `http://localhost:1337/api/<content-type>`

---

## 🧪 Usage

* 👤 **User Login/Registration**
  Secure authentication with role-based logic.

* 📝 **Article Management**
  Authors can create, update, and manage posts via Strapi.

* 💬 **Chat System**
  Users join rooms and exchange real-time messages using Flask-SocketIO.

---

## 🧱 Code Structure Overview

| Module            | Description                        |
| ----------------- | ---------------------------------- |
| `/routes/auth.py` | Handles login/registration         |
| `/templates/`     | HTML templates (Jinja2)            |
| `/static/`        | CSS, JS, and frontend assets       |
| `/socket.py`      | WebSocket logic for real-time chat |
| `/api/strapi.py`  | Integrates Flask with Strapi APIs  |

---

## 📌 Notes

* Ensure `Strapi` and `Flask` servers are running **simultaneously**.
* Check your `Config` class in Flask for correct database settings.
* This project was developed for **educational purposes** as part of the **CS50x curriculum**.
* All code adheres to the [CS50 Academic Honesty Policy](https://cs50.harvard.edu/x/honesty/).

---

## 🙌 Acknowledgements

* Huge thanks to **Harvard University** and **CS50 staff** for creating this incredible course.
* Built with 💡, 🔧, and 🧠 by a passionate learner applying real-world skills.

---

> 📌 *Feel free to explore, modify, and enhance this project for your own needs!*
