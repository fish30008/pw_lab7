from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import timedelta
from typing import List
import auth
import models
import database

app = FastAPI(
    title="Workout CRUD API",
    description="Lab 7",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TokenRequest(BaseModel):
    role: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in_seconds: int
    role: str


@app.post("/token", response_model=TokenResponse, tags=["Authentication"])
async def login_for_access_token(request: TokenRequest):
    """
    Generate a short-lived JWT token (1 minute expiration).
    Pass a JSON body like: {"role": "admin"} or {"role": "visitor"}
    """
    if request.role not in ["admin", "visitor"]:
        raise HTTPException(status_code=400, detail="Role must be either 'admin' or 'visitor'")
    
    # Create token with 1 minute expiration (as per lab requirements)
    access_token_expires = timedelta(minutes=1)
    access_token = auth.create_access_token(
        data={"role": request.role}, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer", 
        "expires_in_seconds": 60,
        "role": request.role
    }


# Just test

@app.get("/api/test-public", tags=["Test"])
def test_public():
    return {"message": "Anyone can read this"}

@app.get("/api/test-visitor", dependencies=[Depends(auth.require_visitor_or_admin)], tags=["Test"])
def test_visitor_access():
    return {"message": "Hello! You have visitor or admin access (READ allowed)."}

@app.post("/api/test-admin", dependencies=[Depends(auth.require_admin)], tags=["Test"])
def test_admin_access():
    return {"message": "Success! You have admin access (WRITE/DELETE allowed)."}


#### CRUD OPERATIONS =

@app.get("/workouts", response_model=List[models.WorkoutResponse], dependencies=[Depends(auth.require_visitor_or_admin)], tags=["Workouts"])
def read_workouts(skip: int = 0, limit: int = 10):
    return database.get_all_workouts(skip=skip, limit=limit)

@app.get("/workouts/{workout_id}", response_model=models.WorkoutResponse, dependencies=[Depends(auth.require_visitor_or_admin)], tags=["Workouts"])
def read_workout(workout_id: str):

    workout = database.get_workout_by_id(workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return workout

@app.post("/workouts", response_model=models.WorkoutResponse, status_code=201, dependencies=[Depends(auth.require_admin)], tags=["Workouts"])
def create_workout(workout_in: models.WorkoutCreate):
    new_workout = database.create_workout(workout_in.dict())
    return new_workout

@app.patch("/workouts/{workout_id}", response_model=models.WorkoutResponse, dependencies=[Depends(auth.require_admin)], tags=["Workouts"])
def update_workout(workout_id: str, workout_in: models.WorkoutUpdate):

    updated_workout = database.update_workout(workout_id, workout_in.dict(exclude_unset=True))
    if updated_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return updated_workout

@app.delete("/workouts/{workout_id}", status_code=204, dependencies=[Depends(auth.require_admin)], tags=["Workouts"])
def delete_workout(workout_id: str):
    """
    Delete a workout by ID. Allowed for: Admins only
    """
    workout = database.get_workout_by_id(workout_id)
    if workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    
    database.delete_workout(workout_id)
    return None
