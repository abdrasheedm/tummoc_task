import uvicorn

if __name__ == '__main__':
    uvicorn.run("Teacher_Student_CRUD.main:app", port = 8000, reload = True)