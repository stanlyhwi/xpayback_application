from api.task1.views import router as task1_router
from api.task2.views import router as task2_router
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return ("welcome to tasks")


app.include_router(task1_router)
app.include_router(task2_router)
