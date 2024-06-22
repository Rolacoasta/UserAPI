Here's the updated `README.md` including the installed packages from your `pip list`:

# Flask User API

This project is a simple Flask-based API for managing user data with CRUD operations.

## Project Setup

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone the repository:
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name


2. Create and activate a virtual environment:
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`


3. Install the dependencies:
   pip install Flask Flask-SQLAlchemy
   

### Installed Packages

Here are the packages installed in the virtual environment:

- blinker 1.8.2
- click 8.1.7
- colorama 0.4.6
- Flask 3.0.3
- Flask-SQLAlchemy 3.1.1
- greenlet 3.0.3
- iniconfig 2.0.0
- itsdangerous 2.2.0
- Jinja2 3.1.4
- MarkupSafe 2.1.5
- packaging 24.0
- pip 24.0
- pluggy 1.5.0
- pytest 8.2.1
- setuptools 70.0.0
- SQLAlchemy 2.0.30
- typing_extensions 4.12.1
- Werkzeug 3.0.3

### Configuration

The application uses SQLite as the database. The database file is named `users.db` and is configured in `app.py`.

## Running the Application

1. Start the Flask application:
   flask run

2. Access the application:
   - Health Check: `GET /health`
   - Home: `GET /`

## Endpoints

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Description**: Returns the health status of the API.

### Root
- **URL**: `/`
- **Method**: GET
- **Description**: Returns a welcome message.

### Create User
- **URL**: `/users`
- **Method**: POST
- **Description**: Creates a new user.
- **Request Body**:
  ```json
   {
      "name": "John Doe",
      "email": "john@example.com"
   }
   ```
- **Responses:**:
   `201 Created`: User successfully created.
   `400 Bad Request`: Invalid input or email already exists


## Database

### User Model
- **Fields**:
  - `id` (Integer, Primary Key)
  - `name` (String, not nullable)
  - `email` (String, unique, not nullable)

### Initializing the Database
The database is initialized automatically when the application runs for the first time.

## Testing
Instructions on how to run tests will be added here once the tests are implemented.


