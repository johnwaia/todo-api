import os
import tempfile
import pytest

import app as app_module


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app_module.DB_PATH = db_path
    app_module.app.config['TESTING'] = True

    app_module.init_db()

    with app_module.app.test_client() as client:
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def test_get_todos_empty(client):
    response = client.get('/todos')
    assert response.status_code == 200
    assert response.get_json() == []


def test_create_todo(client):
    response = client.post('/todos', json={
        'title': 'Apprendre DevSecOps',
        'description': 'Module 4 TP'
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == 'Apprendre DevSecOps'
    assert data['description'] == 'Module 4 TP'
    assert data['done'] is False
    assert 'id' in data


def test_create_todo_missing_title(client):
    response = client.post('/todos', json={
        'description': 'Sans titre'
    })
    assert response.status_code == 400
    assert response.get_json()['error'] == 'Title is required'


def test_get_todo_by_id(client):
    create_response = client.post('/todos', json={'title': 'Tâche test'})
    todo_id = create_response.get_json()['id']

    response = client.get(f'/todos/{todo_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['id'] == todo_id
    assert data['title'] == 'Tâche test'


def test_get_todo_not_found(client):
    response = client.get('/todos/9999')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Todo not found'


def test_update_todo(client):
    create_response = client.post('/todos', json={'title': 'Avant maj'})
    todo_id = create_response.get_json()['id']

    response = client.put(f'/todos/{todo_id}', json={
        'title': 'Apprendre DevSecOps - Mise à jour',
        'description': 'Mise à jour',
        'done': True
    })
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Todo updated'

    updated = client.get(f'/todos/{todo_id}').get_json()
    assert updated['title'] == 'Apprendre DevSecOps - Mise à jour'
    assert updated['done'] is True


def test_update_todo_not_found(client):
    response = client.put('/todos/9999', json={'title': 'Inexistant'})
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Todo not found'


def test_delete_todo(client):
    create_response = client.post('/todos', json={'title': 'À supprimer'})
    todo_id = create_response.get_json()['id']

    response = client.delete(f'/todos/{todo_id}')
    assert response.status_code == 200
    assert response.get_json()['message'] == 'Todo deleted'

    get_response = client.get(f'/todos/{todo_id}')
    assert get_response.status_code == 404


def test_delete_todo_not_found(client):
    response = client.delete('/todos/9999')
    assert response.status_code == 404
    assert response.get_json()['error'] == 'Todo not found'
