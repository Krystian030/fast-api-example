import uvicorn


if __name__ == "__main__":
    HOST = "localhost"
    PORT = 5000
    RELOAD = False
    uvicorn.run("app:app", host=HOST, port=PORT, reload=RELOAD)
