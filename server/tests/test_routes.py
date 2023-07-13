import io

def test_signup(client):
    # Setup
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    # Exercise
    response = client.post('/signup', json=data)
    
    # Verify
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'

def test_login(client):
    # Arrange
    mock_request_data = {
        "username": "testuser",
        "password": "testpassword"
    }

    # Act
    response = client.post('/login', json=mock_request_data)

    # Assert
    assert response.status_code == 200
    assert 'token' in response.get_json()

def test_post(client, app):
    # Log in and get a token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    login_response = client.post('/login', json=login_data)
    token = login_response.json['token']

    # Setup
    data = {
        'file': (io.BytesIO(b"abcdef"), 'test.csv'),
        'title': 'Test Post',
        'description': 'This is a test post'
    }

    # Exercise
    response = client.post('/post', data=data, headers={'Authorization': f"Bearer {token}"})

    # Verify
    assert response.status_code == 201


def test_get_posts(client, app):
    # Log in and get a token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    login_response = client.post('/login', json=login_data)
    token = login_response.json['token']

    # Exercise
    response = client.get('/posts', headers={'Authorization': f"Bearer {token}"})

    # Verify
    assert response.status_code == 200


def test_get_post(client, app):
    # Setup
    post_id = 1  # Use an actual ID from your test database

    # Exercise
    response = client.get(f'/posts/{post_id}', headers={'Authorization': f"Bearer {app.config['SECRET_KEY']}"})

    # Verify
    assert response.status_code == 200
    # Add additional checks as necessary

