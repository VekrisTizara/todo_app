from fastapi import FastAPI
from .schemas import Task
from bson.objectid import ObjectId
from .auth.google_oauth import router
from .db import db

app = FastAPI()
app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/tasks")
async def create_task(task_name, task_description):
    insert_result = db.tasks.insert_one(
        {
            "title": task_name,
            "description": task_description,
            "status": "not_completed",
        }
    )
    return insert_result.inserted_id

@app.get("/tasks")
async def show_tasks(page_num:int=0, page_size:int=25):
    start_index = page_num * page_size
    end_index = start_index + page_size - 1
    results = list(db.tasks.find()[start_index:end_index])
    all_id_prop_to_str(results)
    return {
        "results" : results
    }

@app.put("/tasks")
async def edit_tasks(task:Task):
    db.tasks.update_one(
        {"_id" : ObjectId(task.id)},
        {"$set": {
            "title" : task.title,
            "description" : task.description,
            "status" : task.status,
        }}
    )


@app.delete("/tasks")
async def delete_task(task_id):
    db.tasks.delete_one({"_id" : ObjectId(task_id)})


def all_id_prop_to_str(id_objects):
    for obj in id_objects:
        obj["id"] = str(obj["_id"])
        del obj["_id"]