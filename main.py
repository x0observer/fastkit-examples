import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.middleware.engine import init_db

from src.app.files.register import file_router
from src.app.trip.register import trip_router
from setup import (SERVER_HOST, SERVER_PORT, RELOAD, TIMEOUT_KEEP_ALIVE)




app = FastAPI(
    debug=True,
    docs_url=os.getenv('DOCS_URL', '/docs'),
    redoc_url=os.getenv('REDOC_URL', '/redoc')
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(file_router)
app.include_router(trip_router)

@app.on_event("startup")
async def startup_event():
    """
    Perform startup actions, like initializing the database.
    """
    await init_db()

# # Main entry point for running the app
# if __name__ == "__main__":
#     # Run the application using Uvicorn
#     uvicorn.run(app,
#                 host=SERVER_HOST,
#                 port=SERVER_PORT,
#                 reload=RELOAD,
#                 timeout_keep_alive=TIMEOUT_KEEP_ALIVE
#                 )
