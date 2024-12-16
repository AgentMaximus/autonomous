from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hello": "World"}

# To run this application, execute the command:
# uvicorn fastapi_app:app --reload
# Ensure you have uvicorn installed with: pip install uvicorn