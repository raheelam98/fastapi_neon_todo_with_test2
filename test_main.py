from fastapi.testclient import TestClient
from fastapi_neon_todo1.main import app

from fastapi_neon_todo1.model import test_create_db_tables,test_engine, get_session, Todo

import pytest
from sqlmodel import Session

# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/?h=test

# create session for test
@pytest.fixture(name="session")
def session_fixture():
    test_create_db_tables()
    with Session(test_engine) as session:   
        yield session

# Create the new fixture named "client"
@pytest.fixture(name="client") 
def client_fixture(session : Session):  # This client fixture, in turn, also requires the session fixture.

    # Define the new function that will be the new dependency override.
    def get_session_override():
        return session 
    
    # Here's where we create the custom session object for this test in a with block.
    # It uses the new custom engine we created, so anything that uses this session will be using the testing database.
    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    
    # we can restore the application back to normal, by removing all the values in this dictionary app.dependency_overrides. 
    app.dependency_overrides.clear()
        
# function to read main file
def test_read_main():
    #create TestClind for the fastapi app
    clinet = TestClient(app=app)
    response = clinet.get('/')
    assert response.status_code == 200
    assert response.json() == {"Fast API": "Todo"}
    
###### ====================  Get Data From Test Database ====================  ====================

###### get todo from test-db
def test_get_todo(client : TestClient):
    response = client.get('/get_todos')
    assert response.status_code == 200

###### ====================  Add Data Into Test Database ====================  ====================

###### add data into test-db
def test_create_todo(client: TestClient): 
    new_todo = 'Modern Python'

    response = client.post("/create_todo_test/" ,json=new_todo)
    assert response.status_code == 200

###### ====================  Delete Data From Test Database ====================  ====================

###### delete data from test-db
def test_delete_todo(client : TestClient):
        
        todo_id = 18
        response = client.delete(f'/delete_todo_hero/{todo_id}')

        assert response.status_code == 200

        for ids in response.json():
            assert  ids
            print(ids)
    
# #         #https://sqlmodel.tiangolo.com/tutorial/delete/
# #         #https://sqlmodel.tiangolo.com/tutorial/fastapi/delete/?h=dele
  
###### ====================  Update Data From Test Database ====================  ====================

##### update data from test-db
def test_update_todo(client : TestClient):
   
    id = 16  # todo_id for testing
    test_name = "Generative AI"  # update todo name

    # Make the PUT request
    response = client.put(f'/update_todo_test?todo_id={id}', json=test_name)

    # Check the response
    assert response.status_code == 200  
    
###### ====================  Update Data From Test Database ====================  ====================

#####  update data from test-db
def test_update_todo_new2(client : TestClient):
   
    id = 10  # todo_id for testing
    todo_name = "CSS"  # update todo name

    # Make the PUT request
    response = client.put(f'/update?id={id}', json=todo_name)

    # Check the response
    assert response.status_code == 200
  

###### ====================  tutorial points ====================  ====================
    
# Piaic GitHub
# learn-generative-ai/05_microservices_all_in_one_platform/11_microservice_db        
# https://github.com/panaverse/learn-generative-ai/tree/main/05_microservices_all_in_one_platform/11_microservice_db        

# Test Applications with FastAPI and SQLModel    
# https://sqlmodel.tiangolo.com/tutorial/fastapi/tests/    
    
# use this client to talk to the API and send a POST HTTP operation, creating a new hero.
# response = client.post( "/heroes/", json={"name": "Deadpond", "secret_name": "Dive Wilson"})

# Then we get the JSON data from the response and put it in the variable data.    
# data = response.json()

# Next we start testing the results with assert statements, we check that the status code of the response is 200
# assert response.status_code == 200 
  
# Error :- assert 404 == 200,  E +  where 404 = <Response [404 Not Found]>.status_code
# Error :- assert 422 == 200,  E +  where 422 = <Response [422 Unprocessable Entity]>.status_code    
    
# .get() method: The .get() method allows you to retrieve a value from a dictionary based on a key. If the key doesn’t exist, it returns a default value (or None if not specified):

# The 404 (Not Found) status code indicates that the origin server did not find a current representation 
# for the target resource or is not willing to disclose that one exists. A 404 status 
# code does not indicate whether this lack of representation is temporary or permanent;    
# Testing    
# https://fastapi.tiangolo.com/tutorial/testing/    
    
# ====================  tutorial points ====================  ====================

         
    
  

