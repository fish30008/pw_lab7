import json
import uuid
import os

DB_FILE = "workouts.json"
#empty list if file doesn't exist or is invalid
DEFAULT_WORKOUTS = []

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump(DEFAULT_WORKOUTS, f, indent=2)
        return DEFAULT_WORKOUTS
    with open(DB_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_WORKOUTS

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=2)

def get_all_workouts(skip: int = 0, limit: int = 100):
    db = load_db()
    return db[skip : skip + limit]

def get_workout_by_id(workout_id: str):
    db = load_db()
    return next((w for w in db if w["id"] == workout_id), None)

def create_workout(workout_data: dict):
    db = load_db()
    workout_dict = workout_data.copy()
    workout_dict["id"] = str(uuid.uuid4())
    workout_dict["liked"] = False
    db.insert(0, workout_dict)
    save_db(db)
    return workout_dict

def update_workout(workout_id: str, update_data: dict):
    db = load_db()
    workout = next((w for w in db if w["id"] == workout_id), None)
    if workout:
        # Update only fields that are provided
        for key, value in update_data.items():
            if value is not None:
                workout[key] = value
        save_db(db)
        return workout
    return None

def delete_workout(workout_id: str):
    db = load_db()
    new_db = [w for w in db if w["id"] != workout_id]
    if len(new_db) == len(db):
        return False
    save_db(new_db)
    return True


if __name__ == "__main__":
    # Initialize the database with default workouts if it doesn't exist
    load_db()