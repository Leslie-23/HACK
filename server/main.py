from fastapi import FastAPI
from server.routes.example import router as example_router

# Initialize FastAPI app
app = FastAPI()

# Include the example route
app.include_router(example_router)
