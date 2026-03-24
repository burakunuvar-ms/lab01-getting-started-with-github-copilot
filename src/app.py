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
    },
    "Swimming Team": {
        "description": "Competitive and recreational swimming training at UvA sports center",
        "schedule": "Mondays and Fridays, 6:00 PM - 7:30 PM",
        "max_participants": 30,
        "participants": ["thomas@student.uva.nl", "lisa@student.uva.nl"]
    },
    "Football Club": {
        "description": "Join our football community for friendly matches and training sessions",
        "schedule": "Sundays, 2:00 PM - 4:00 PM",
        "max_participants": 22,
        "participants": ["marco@student.uva.nl", "elena@student.uva.nl"]
    },
    "Photography Workshop": {
        "description": "Learn photography techniques and explore Amsterdam's visual storytelling",
        "schedule": "Saturdays, 2:00 PM - 4:00 PM",
        "max_participants": 12,
        "participants": ["aisha@student.uva.nl", "david@student.uva.nl"]
    },
    "Theatre & Drama Club": {
        "description": "Perform in plays, improv, and creative theatrical productions",
        "schedule": "Wednesdays, 7:00 PM - 9:00 PM",
        "max_participants": 18,
        "participants": ["emma@student.uva.nl", "olaf@student.uva.nl"]
    },
    "Philosophy Discussion Group": {
        "description": "Engage in deep philosophical conversations and debate contemporary issues",
        "schedule": "Thursdays, 5:30 PM - 7:00 PM",
        "max_participants": 20,
        "participants": ["nina@student.uva.nl", "tobias@student.uva.nl"]
    },
    "Environmental Science Club": {
        "description": "Research and action group focused on sustainability and climate science",
        "schedule": "Tuesdays, 6:00 PM - 7:30 PM",
        "max_participants": 16,
        "participants": ["lars@student.uva.nl", "yuki@student.uva.nl"]
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

    # Validate student is not already signed up
    if email in activity["participants"]:
        raise HTTPException(status_code=400, detail="Student already signed up for this activity")  
    
    # Add student
    activity["participants"].append(email)
    return {"message": f"Signed up {email} for {activity_name}"}
