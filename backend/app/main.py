from fastapi import FastAPI

app = FastAPI(title="LexiCore API")

@app.get("/")
def root():
    return {"message": "LexiCore API is running"}