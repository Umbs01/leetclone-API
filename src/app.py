from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import auth, problems, run_code, users, submit

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
app.include_router(run_code.router)
app.include_router(users.router)
app.include_router(submit.router)

@app.get("/")
def read_root():
    return {"message": "This is the root of the API"}
