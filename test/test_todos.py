from fastapi import status
from ..routers.todos import get_db, get_current_user
import os
from .utils import *     #import everything present in utils
from ..models import Todos

app.dependency_overrides[get_db]  = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user



#Testing this function to test the GET api from todos.py
def test_read_all_authenticated(test_todo):
    response = client.get("/todo")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{"complete" : False, "title": "Learn to code",
        "description":"Need to learn everyday!", 'id':1,
        "priority" : 5,  "owner_id" : 1}]

def test_read_one_authenticated_passes(test_todo):
    response = client.get("/todo/get/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"complete" : False, "title": "Learn to code",
        "description":"Need to learn everyday!", 'id':1,
        "priority" : 5,  "owner_id" : 1}

def test_for_one_Authentication_fails():
    response  = client.get("/todo/get/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "table not found"}


#Testing this function to test the POST api from todos.py
def test_create_todo(test_todo):
    request_data = {
        "title": "Learn to code",
        "description" : "Need to learn everyday!",
        "priority" : 5,
        "complete" : False
    }

    response = client.post('/todo/create', json = request_data)
    assert response.status_code == 201

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get('title')
    assert model.description == request_data.get('description')
    assert model.priority == request_data.get('priority')
    assert model.complete == request_data.get('complete')

#Testing this function to test the PUT api not present from todos.py
def test_update_todo(test_todo):
    request_data = {
        "title": "change the title of todo already saved!",
        "description": "Need to learn everyday!",
        "priority": 5,
        "complete": False,
    }

    response = client.put("/todo/update/1", json = request_data)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id== 1).first()
    assert model.title == "change the title of todo already saved!"



#Testing this function to test the PUT api not present from todos.py

def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "change the title of todo already saved!",
        "description" : "Need to learn everyday!",
        "priority" : 5,
        "complete" : False,
    }
    response = client.put('/todo/update/999', json = request_data)
    assert response.status_code == 404
    assert response.json() == {'detail': 'table not found'}


def test_delete_todo(test_todo):
    response = client.delete('/todo/delete/1')
    print(response)
    assert response.status_code == 204
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None

def test_delete_not_found():
    response = client.delete('/todo/delete/999')
    print(response)
    assert response.status_code == 404
    assert response.json() == {'detail': 'no data found'}