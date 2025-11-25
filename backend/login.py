from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from auth_system import AuthSystem

app = FastAPI()

# 1. SETUP CORS
# This allows your React app (running on port 3000) to talk to this API
origins = [
    "http://localhost:3000",  # React Default
    "http://localhost:5173",  # Vite React Default
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database
auth_system = AuthSystem()

# --- Pydantic Models (Data Validation) ---
class SignupRequest(BaseModel):
    full_name: str
    username: str
    email: str
    password: str
    confirm_password: str

class LoginRequest(BaseModel):
    identifier: str
    password: str

# --- API ROUTES ---

@app.get("/")
def read_root():
    return {"message": "FastAPI Authentication Server is Running!"}

@app.post("/api/signup")
async def signup(data: SignupRequest):
    """
    Receives JSON: { "full_name": "...", "username": "...", ... }
    Returns JSON: { "message": "..." } or Error
    """
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Passwords do not match"
        )

    try:
        # We access data.variable_name because it's now a Pydantic object
        auth_system.register_user(
            data.full_name, 
            data.username, 
            data.email, 
            data.password
        )
        return {"message": "Account created successfully", "user": data.username}
    
    except ValueError as e:
        # Send 400 Error so React knows it failed
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=str(e)
        )

@app.post("/api/login")
async def login(data: LoginRequest):
    """
    Receives JSON: { "identifier": "user@email.com", "password": "..." }
    """
    user = auth_system.authenticate_user(data.identifier, data.password)
    
    if user:
        # In a real app, you would return a JWT Token here.
        # For a hackathon, returning the user info is okay.
        return {
            "message": "Login successful",
            "user_id": user.id,
            "full_name": user.full_name,
            "username": user.username
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Credentials"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)