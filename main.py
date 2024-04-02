from fastapi import FastAPI, Depends, HTTPException, Body
from fastapi_neon_todo1.model import create_db_and_tables, Todo, engine, get_session
from sqlmodel import Session, select
from typing import Annotated

async def life_span(app: FastAPI):
    print("Crate table.... ")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=life_span, title="Todo App")

@app.get('/')
def get_root_route():
    return {"Fast API": "Todo"}

# get todo from database
def get_db_todo():
    with Session(engine) as session:
        get_todos = select(Todo)
        todo_list = session.exec(get_todos).all()
        if not todo_list:
            return "Todo Not Found"
        else:
            return todo_list
        
@app.get('/get_todos', response_model=list[Todo])
def read_todos(session: Annotated[Session, Depends(get_session)]):
    todo_list = get_db_todo()
    if not todo_list:
        raise HTTPException(status_code=404, detail=(f"Todo Not Found In DB"))
    else:
        return todo_list

# # insert data into Todo
def create_db_todo(todo_name : str):
    with Session(engine) as session:
        todos = Todo(todo_name=todo_name)
        if not todos:
            raise HTTPException(status_code=404, detail=(f"Cannot Add Todo In DB"))
        else:
            session.add(todos)
            session.commit()
            session.refresh(todos)
            return todos
    
@app.post('/add_todo/', response_model=Todo) 
def add_todo_route(todo_name :Annotated[str, Body()], session: Annotated[Session,Depends(get_session) ]):
    added_todo = create_db_todo(todo_name)
    return added_todo
       
def update_db_todo(id:int, todo_name:str, session):
    selected_todo = select(Todo).where(Todo.id == id)
    update_todo = session.exec(selected_todo).first()
    if not update_todo:
        raise HTTPException(status_code=404, detail=(f"Todo Id: {id} Not Found In DB"))
    else:
        update_todo.todo_name = todo_name
        session.add(update_todo)
        session.commit()
        session.refresh(update_todo)
        return update_todo 
    
@app.put('/update', response_model=Todo)   
def update_todo_route(id: int, todo_name: Annotated[str, Body()], session: Annotated[Session, Depends(get_session)] ):
    updated_todo = update_db_todo(id, todo_name, session)
    if not updated_todo:
        raise HTTPException(status_code=404, detail=f"User with id: {id} does not exist....")
    return updated_todo  # return the updated todo instead of the function itself    
    
def delete_db_todo(todo_id : int):
    with Session(engine) as session:
        #db_todo = session.get(Todo, id)
        db_todo = session.get(Todo, todo_id)
        if not db_todo:
            raise HTTPException(status_code=404, detail=(f"Todo Id: {todo_id} Not Found In DB"))
        session.delete(db_todo)
        session.commit()
        return db_todo
        todo_list = session.exec(select(Todo)).all()

@app.delete('/delete_todo/{todo_id}', response_model=Todo)
async def delete_todo_route(todo_id: int , session : Annotated[Session,Depends(get_session)]):
    delete_todo = delete_db_todo(todo_id)
    if not delete_todo:
        raise HTTPException(status_code=404, detail="Todo Not Found...")
    return delete_todo
    todo_list = session.exec(select(Todo)).all()


#### ==================== test code  ==================== #####  

@app.post("/create_todo_test")
async def create_todo(todo: Annotated[str, Body()], session: Annotated[Session, Depends(get_session)]):
    todos = Todo(todo_name=todo)
    session.add(todos)
    session.commit()
    session.refresh(todos)
    return todos

#### ==================== test code ==================== #####  

#https://sqlmodel.tiangolo.com/tutorial/delete/
#https://sqlmodel.tiangolo.com/tutorial/fastapi/delete/?h=dele


@app.delete("/delete_todo_hero/{todo_id}/")
def delete_todo(todo_id: int, session: Annotated[Session, Depends(get_session)]):   
    todo_sel = session.get(Todo, todo_id)
    if not todo_sel:
        raise HTTPException(status_code=404, detail=(f'Todo ID {todo_id} Not Found In DB'))
    session.delete(todo_sel)
    session.commit()
    return todo_sel
    #todo_list = session.exec(select(Todo)).all()


#### ==================== test code ==================== #####  

@app.put("/update_todo_test", response_model=Todo)
async def update_todo(todo_id : int, todo_name :Annotated[str, Body()], session: Annotated[Session, Depends(get_session)]):
     get_id : Todo = select(Todo).where(Todo.id == todo_id)
     update_todo = session.exec(get_id).first()
     if not update_todo:
        raise HTTPException(status_code=404, detail=(f"Todo Id: {todo_id} Not Found In DB"))
     else:
        update_todo.todo_name = todo_name
        session.add(update_todo)
        session.commit()
        session.refresh(update_todo)
        return  update_todo
        todo_list = session.exec(select(Todo)).all()



