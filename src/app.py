"""
University of Amsterdam Student Activities API

A FastAPI application that allows students of University of Amsterdam
to view and sign up for extracurricular activities.
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
import os
from pathlib import Path

app = FastAPI(
    title="University of Amsterdam Activities API",
    description="API for viewing and signing up for extracurricular activities at University of Amsterdam"
)

# Mount the static files directory
app.mount(
    "/static",
    StaticFiles(directory=os.path.join(Path(__file__).parent, "static")),
    name="static"
)

# In-memory activity database
activities = {
    "Cycling Club": {
        "description": "Explore Amsterdam's iconic canals and streets on two wheels",
        "schedule": "Saturdays, 9:00 AM - 11:00 AM",
        "max_participants": 20,
        "participants": ["anna@student.uva.nl", "lucas@student.uva.nl"]
    },
    "Dutch Language Circle": {
        "description": "Practice conversational Dutch with fellow international students",
        "schedule": "Wednesdays, 5:00 PM - 6:30 PM",
        "max_participants": 15,
        "participants": ["mei@student.uva.nl", "carlos@student.uva.nl"]
    },
    "Data Science Society": {
        "description": "Collaborative projects and workshops on data analysis and machine learning",
        "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
        "max_participants": 25,
        "participants": ["sofia@student.uva.nl", "james@student.uva.nl"]
    }
}


@app.get("/")
def root():
    return RedirectResponse(url="/static/index.html")


@app.get("/activities")
def get_activities():
    return activities


@app.post("/activities/{activity_name}/signup")
def signup_for_activity(activity_name: str, email: str):
    """Sign up a student for an activity"""
    # Validate activity exists
    if activity_name not in activities:
        raise HTTPException(status_code=404, detail="Activity not found")

    # Get the specific activity
    activity = activities[activity_name]

    # Check if activity is full
    if len(activity["participants"]) >= activity["max_participants"]:
        raise HTTPException(status_code=400, detail="Activity is full")

    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
