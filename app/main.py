from fastapi import FastAPI
# from .routes.tasks import task_router
# from .routes.auth import auth_router

app = FastAPI()

@app.get("/")
def home():
    return {"message": "TO DO API IS WORKING PROPERLY"}

# app.include_router(task_router)
# app.include_router(auth_router,tags=["AUTHENTICATION_ROUTES"])