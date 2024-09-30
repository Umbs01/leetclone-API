from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, problems

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Authorization"]
)

app.include_router(auth.router) 
app.include_router(problems.router)

@app.get("/")
def read_root():
    return {"message": "This is the root of the API"}
