from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import os

app = Flask(__name__)

# Configure the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'users.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)

# ================================
#           ENDPOINTS
# ================================

# Health check route to verify the API is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200

# Root route that returns a welcome message
@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the Flask API!"}), 200

# Endpoint to create a new user
@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()  # Extract JSON data from the request body
    except:
        return jsonify({"error": "Invalid JSON format"}), 400  # Handle invalid JSON format

    try:
        if not data or 'name' not in data or 'email' not in data:  # Validate the input data
            return jsonify({"error": "Invalid input"}), 400

        if User.query.filter_by(email=data['email']).first():  # Check for existing email
            return jsonify({"error": "Email already exists"}), 400

        new_user = User(name=data['name'], email=data['email'])  # Create a new User object
        db.session.add(new_user)  # Add the new user to the database session
        db.session.commit()  # Commit the session to save the user

        return jsonify({"id": new_user.id, "name": new_user.name, "email": new_user.email}), 201  # Return the new user's details
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500  # General error handling

# Endpoint to retrieve a user by their ID
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    try:
        user = db.session.get(User, id)

        if user is None:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint to return all users in the database
@app.route('/users', methods=['GET'] )
def get_all_users():
    try:
        users = User.query.all()
        user_list = [{"id": user.id, "name": user.name, "email": user.email} for user in users]
        return jsonify(user_list), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint to return the number count of all users in the database.
@app.route('/users/count', methods=['GET'])
def get_user_count():
    try:
        count = db.session.query(func.count(User.id)).scalar()
        return jsonify({"count": count}), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint to update a user (PUT /users/<id>)
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        data = request.get_json()

        if not data or 'name' not in data or 'email' not in data:
            return jsonify({"error": "Invalid input"}), 400
        
        user = db.session.get(User, id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.name = data['name']
        user.email = data['email']

        db.session.commit()

        return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200
    
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint to delete a user (DELETE /users/<id>)
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    try:
        user = db.session.get(User, id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "User deleted"}), 200
    
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    os.makedirs(app.instance_path, exist_ok=True)
    app.run(debug=True)
