import pytest
import sys
import os

# Ensure the app module can be found by adding the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, db, User

# Fixture to set up the test client and in-memory SQLite database
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create all database tables
            yield client  # Provide the test client to the tests
            db.drop_all()  # Drop all database tables after tests

# Test to ensure the health check endpoint is working correctly
def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json == {"status": "healthy"}

# Test to check if a new user can be created successfully
def test_create_user(client):
    response = client.post('/users', json={'name': 'John Doe', 'email': 'john@example.com'})
    assert response.status_code == 201
    assert response.json['name'] == 'John Doe'
    assert response.json['email'] == 'john@example.com'

# Test to check if an existing user can be retrieved
def test_get_user(client):
    user = User(name='Jane Doe', email='jane@example.com')
    db.session.add(user)
    db.session.commit()

    response = client.get(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Jane Doe'
    assert response.json['email'] == 'jane@example.com'

# Test to check if all users can be retrieved
def test_get_all_users(client):
    user1 = User(name='John Doe', email='john@example.com')
    user2 = User(name='Jane Doe', email='jane@example.com')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    response = client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 2

# Test to check if the user count can be retrieved
def test_get_user_count(client):
    user1 = User(name='John Doe', email='john@example.com')
    user2 = User(name='Jane Doe', email='jane@example.com')
    db.session.add(user1)
    db.session.add(user2)
    db.session.commit()

    response = client.get('/users/count')
    assert response.status_code == 200
    assert response.json['count'] == 2

# Test to check if an existing user's details can be updated
def test_update_user(client):
    user = User(name='John Doe', email='john@example.com')
    db.session.add(user)
    db.session.commit()

    response = client.put(f'/users/{user.id}', json={'name': 'Johnny Doe', 'email': 'johnny@example.com'})
    assert response.status_code == 200
    assert response.json['name'] == 'Johnny Doe'
    assert response.json['email'] == 'johnny@example.com'

# Test to check if an existing user can be deleted
def test_delete_user(client):
    user = User(name='John Doe', email='john@example.com')
    db.session.add(user)
    db.session.commit()

    response = client.delete(f'/users/{user.id}')
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted'
