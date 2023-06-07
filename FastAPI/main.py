import uvicorn

if __name__ == '__main__':
    uvicorn.run("tummoc_task.main:app", port = 9000, reload = True)