# CS50x Final Project: Web Application with Flask and Strapi

#### Video Demo: https://youtu.be/WWoUpCO7WGg

#### Description:
This project is a web application that allows users to authenticate, create and manage content, and communicate in real-time. The backend is powered by Flask, with user data managed in a local SQLite database, and content management handled through the Strapi CMS.

## Features:
- User authentication and registration
- Role-based access control (viewer and author)
- Content management system integrated with Strapi
- Real-time chat functionality using Socket.IO
- User profile management
- Dynamic content fetching from Strapi

## Technologies Used:
- Flask
- Flask-SocketIO
- SQLite
- Strapi
- HTML, CSS, and Bootstrap for the frontend
- Python for backend development

## Installation and Setup:

### Prerequisites:
- Ensure you have [Node.js](https://nodejs.org/) installed (version >=18.0.0 and <=20.x.x).
- Install [Yarn](https://classic.yarnpkg.com/en/docs/install) as a package manager.
- Install [Python](https://www.python.org/downloads/) (preferably version 3.8 or higher).
- Install [Flask](https://flask.palletsprojects.com/en/2.0.x/installation/) and other required Python packages.

### Steps to Run the Project:

1. **Set Up the Flask Backend:**
   - Create a virtual environment:
     ```bash
     python -m venv venv
     source venv/bin/activate  # On Windows use `venv\Scripts\activate`
     ```
   - Install the required packages:
     ```bash
     pip install -r requirements.txt
     ```

2. **Set Up Strapi:**
   - Navigate to the Strapi directory:
     ```bash
     cd Strapi
     ```
   - Install Strapi dependencies:
     ```bash
     yarn install
     ```
   - Run Strapi in development mode:
     ```bash
     yarn develop
     ```
   - Ensure that your Strapi instance is running on `http://localhost:3000`.

3. **Run the Flask Application:**
   - In a separate terminal, navigate back to your Flask application directory:
     ```bash
     cd path/to/your/flask-app
     ```
   - Start the Flask application:
     ```bash
     flask run
     ```

4. **Access the Application:**
   - Open your web browser and go to `http://127.0.0.1:5000` to access your application.

### Strapi Setup

Strapi is a headless CMS that allows you to manage your content through an API. Follow the steps below to set up Strapi for your project:

1. **Install Node.js**: Make sure you have Node.js installed on your machine. Strapi requires Node.js version `>=18.0.0 <=20.x.x`. You can download it from [Node.js official website](https://nodejs.org/).

2. **Install Yarn**: If you don’t have Yarn installed, you can install it globally using npm:
   npm install -g yarn


3. **Create a Strapi Project**:
   - Navigate to your desired directory in the terminal.
   - Run the following command to create a new Strapi project:
     ```bash
     npx create-strapi-app my-project --quickstart
     ```
   - Replace `my-project` with your desired project name.

4. **Run Strapi**:
   - Change to the newly created project directory:
     ```bash
     cd my-project
     ```
   - Start the Strapi server:
     ```bash
     yarn develop
     ```
   - This will launch Strapi in development mode. You can access the admin panel at `http://localhost:1337/admin`.

5. **Configure Your Database**:
   - By default, Strapi uses SQLite as its database. You can change this to another database (PostgreSQL, MongoDB, etc.) by modifying the `config/database.js` file in your Strapi project.

6. **Create API and Content Types**:
   - Access the Strapi admin panel and log in with the admin user credentials you created.
   - You can create new content types (e.g., articles, users) through the "Content Type Builder" in the Strapi admin panel.
   - After creating content types, you can add fields and set permissions for the APIs.

7. **Setting Permissions**:
   - Navigate to "Settings" > "Roles" in the Strapi admin panel.
   - Set up permissions for the roles you create (e.g., public, authenticated) to define who can access your APIs.

8. **Test Your APIs**:
   - You can test your APIs using tools like Postman or directly from the Strapi admin panel. The API endpoints will be available at `http://localhost:1337/api/<content-type>`.

## Usage:

- **Login and Registration:** Users can create an account or log in to access their profile and the content management system.
- **Content Management:** Users can create and manage articles through the Strapi interface.
- **Chat Room:** Users can join chat rooms and communicate in real-time.

## Code Overview:
The main components of the Flask application are as follows:

- **User Authentication:** Handled through the `/login` and `/register` routes, utilizing password hashing for security.
- **Content Fetching:** Articles are fetched dynamically from the Strapi API and displayed on the frontend.
- **Real-Time Chat:** Implemented using Socket.IO, allowing users to join rooms and send messages to each other.

## Notes:
- Ensure that you have the correct database configuration set up in the `Config` class within your Flask application.
- This application is designed for educational purposes as part of the CS50x course.
