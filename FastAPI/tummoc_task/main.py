from fastapi import FastAPI
from . import models
from .database import engine
from .routers import teacher, student, user, distance


app = FastAPI()

models.Base.metadata.create_all(engine)



# HELLO WORLD
@app.get('/', tags=['Hello world'])
def index():
    return "hello world"


# OTHER ROUTERS
app.include_router(teacher.router)
app.include_router(student.router)
app.include_router(user.router)
app.include_router(distance.router)

