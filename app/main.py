from fastapi import FastAPI
from routes.tasks import router as task_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "TO DO API IS WORKING PROPERLY"}

app.include_router(task_router)