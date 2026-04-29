import uuid

class Database:
    def __init__(self):
        self.workouts = {}

    def get_workout_by_id(self, workout_id):
        return self.workouts.get(workout_id)
