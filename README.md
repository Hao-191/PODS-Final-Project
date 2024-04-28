# Roomio PODS Final Project

## Project Overview
Roomio is a web application developed **individually** using Flask, designed to streamline room management and operations. The application integrates with a MySQL database to store and manage data efficiently.

## Features
- Login & User Session Handle
- Search Certain Apartment Units
- Register Pet
- Post and View Interests
- Display Unit and Building Info
- More Advanced Search of Units
- Search Interest
  
## Code Structure
Below is an overview of the main components of our Flask application's directory and file structure:

### `app.py`
- This is the entry point of our application. It is responsible for configuring and running the Flask application.
- It registers various blueprints that handle different areas of functionality in the application.

### `blueprints/`
- This directory contains different modules, each corresponding to a different blueprint.
- Each module contains routes and views for a specific part of the application.
- Example modules:
  - `auth.py` for authentication related routes.
  - `dashboard.py` for the main dashboard features.

### `utils/`
- Contains utility functions and classes that support the application, particularly with database interactions.
- These utilities are used across different blueprints to execute SQL commands and fetch data.

### `static/`
- This folder holds static files like JavaScript, CSS, and images.
- These files are used to add interactivity and style to the web pages.

### `templates/`
- Contains HTML templates for the application.
- These templates are rendered by Flask to present dynamic data to the user.

### `databaseConnection.py`
- Manages database connections.
- Provides functionality to connect and disconnect from the database.
  
## Getting Started
### Prerequisites
- Python 3.x
- Flask
- MySQL

### Installation
Clone the repository:
`git clone https://github.com/Hao-191/Roomio-PODS-Final-Project.git`

### Setting up the Database
- Ensure MySQL is installed and running on your system.
- Create a database `roomio`, insert the `ProjSchema.sql` to `roomio`, and update the connection in `databaseConnection.py`.

### Running the Application
1. Navigate to the project directory:
`cd Roomio-PODS-Final-Project`

2. Run the Flask application:
`python init.py`
