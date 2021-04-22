from fastapi.testclient import TestClient

from .main import app

client = TestClient(app)


def test_create_thread():
    response = client.post(
        "/thread/",
        json={"users": ["user1", "user2"]},
    )
    assert response.status_code == 200
    assert "thread_id" in response.json()

def test_create_thread_one_user():
    response = client.post(
        "/thread/",
        json={"users": ["user1"]},
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Thread can only be created for 2 or more users"}

def test_create_thread_invalid_data():
    response = client.post(
        "/thread/",
        json={"invalid_users": ["user1", "user2"]},
    )
    assert response.status_code == 422

def test_create_thread_invalid_usernames():
    response = client.post(
        "/thread/",
        json={"users": ["", "qwertyuiopasdfghjklzxcvbnm"]},
    )
    assert response.status_code == 422

def test_post_in_thread_invalid_thread():
    response = client.post(
        "/thread/999999/invalidusername",
        json={"message": "foobar"},
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "Thread with given id not found"}

def test_post_in_thread_invalid_username():
    response = client.post(
        "/thread/1/invalidusername",
        json={"message": "foobar"},
    )
    assert response.status_code == 200
    assert response.json() == {"detail": "User with given username not found"}


def test_post_in_thread_no_permission():
    response = client.post(
        "/thread/",
        json={"users": ["user1", "user2"]},
    )
    first_thread_id = response.json()['thread_id']
    assert response.status_code == 200
    assert first_thread_id != None

    response = client.post(
        "/thread/",
        json={"users": ["user3", "user4"]},
    )
    second_thread_id = response.json()['thread_id']
    assert response.status_code == 200
    assert second_thread_id != None


    response = client.post(
        f"/thread/{first_thread_id}/user3",
        json={"message": "foobar"},
    )
    assert response.status_code == 403
    assert response.json() == {"detail": "User does't have a permission to write in this thread"}

def test_post_in_thread_message_too_long():
    response = client.post(
        "/thread/",
        json={"users": ["user1", "user2"]},
    )
    thread_id = response.json()['thread_id']
    assert response.status_code == 200
    assert thread_id != None

    response = client.post(
        f"/thread/{thread_id}/user1",
        json={"message": "a" * 255},
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Message should be be between 1-200 characters"

def test_post_in_thread_message_empty():
    response = client.post(
        "/thread/",
        json={"users": ["user1", "user2"]},
    )
    thread_id = response.json()['thread_id']
    assert response.status_code == 200
    assert thread_id != None

    response = client.post(
        f"/thread/{thread_id}/user1",
        json={"message": ""},
    )
    assert response.status_code == 422
    assert response.json()['detail'][0]['msg'] == "Message should be be between 1-200 characters"

def test_post_in_thread():
    response = client.post(
        "/thread/",
        json={"users": ["user1", "user2"]},
    )
    thread_id = response.json()['thread_id']
    assert response.status_code == 200
    assert thread_id != None

    response = client.post(
        f"/thread/{thread_id}/user1",
        json={"message": "Test Message"},
    )
    assert response.status_code == 203
    assert response.json() == None

def test_get_messages():
    response = client.post(
        "/thread/",
        json={"users": ["user1", "user2"]},
    )
    thread_id = response.json()['thread_id']
    assert response.status_code == 200
    assert thread_id != None

    response = client.post(
        f"/thread/{thread_id}/user1",
        json={"message": "Test Message"},
    )
    assert response.status_code == 203
    assert response.json() == None

    response = client.get(
        f"/thread/{thread_id}",
    )

    assert response.status_code == 200
    assert response.json() == {"messages": [{"message":"Test Message", "username":"user1"}]}