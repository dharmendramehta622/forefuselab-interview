from typing import Union 
from routers import items 
from fastapi import FastAPI,status

app = FastAPI()

# Include the router
app.include_router(items.router)

@app.get("/")
def read_root():
    return {
            "status":status.HTTP_200_OK,
            "message": "Hello from Forefuse Labs",
        }

