from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine
from routers import clients, cases
# Automatically create the SQLite/PostgreSQL database tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PayAssured Internal CRM",
    description="API for B2B Invoice Recovery and Case Management",
    version="1.0.0"
)

# Crucial for allowing your Node.js frontend to talk to this Python backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allow any origin to send requests. 
    allow_credentials=True, #Allow cookies, if it is false then users can't stay logged in. 
    allow_methods=["*"], #Allows all standard HTTP methods.
    allow_headers=["*"], #Allows all standard HTTP headers.
)

# Register the routes exactly as PayAssured requested them
app.include_router(clients.router, prefix="/clients")
app.include_router(cases.router, prefix="/cases")

@app.get("/")
def health_check():
    return {"status": "System Online", "message": "Welcome to the PayAssured API"}

