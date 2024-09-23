from fastapi import FastAPI

from routes import user_route

app = FastAPI()

# routes config
app.include_router(user_route.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)