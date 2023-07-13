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
    post_data = [
        {
            'file': (io.BytesIO(b"abcdef"), 'test1.csv'),
            'title': 'Test Post 1',
            'description': 'This is a test post 1'
        },
        {
            'file': (io.BytesIO(b"ghijkl"), 'test2.csv'),
            'title': 'Test Post 2',
            'description': 'This is a test post 2'
        },
        {
            'file': (io.BytesIO(b"mnopqr"), 'test3.csv'),
            'title': 'Test Post 3',
            'description': 'This is a test post 3'
        },
    ]

    for data in post_data:
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
    
def test_delete_post(client, app):
    # Log in and get a token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    login_response = client.post('/login', json=login_data)
    token = login_response.json['token']

    # Get posts of the user
    response = client.get('/posts', headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    posts = response.get_json()

    if not posts:
        pytest.skip("No posts found for the user to delete")

    # Setup
    post_id = posts[0]['id']  # Use the ID of the first post

    # Exercise
    response = client.delete(f'/posts/{post_id}', headers={'Authorization': f"Bearer {token}"})

    # Verify
    assert response.status_code == 200
    assert response.json['message'] == 'Post deleted successfully'


def test_delete_user(client, app):
    # Log in and get a token
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    login_response = client.post('/login', json=login_data)
    token = login_response.json['token']

    # Exercise
    response = client.delete('/user', headers={'Authorization': f"Bearer {token}"})

    # Verify
    assert response.status_code == 200
    assert response.json['message'] == 'User and all related posts deleted successfully'


