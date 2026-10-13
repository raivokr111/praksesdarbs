from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from api import db

BASE = Path(__file__).parent
app = FastAPI()
app.mount("/static", StaticFiles(directory=BASE / "static"), name="static")
templates = Jinja2Templates(directory=BASE / "templates")


class Score(BaseModel):
    name: str
    score: int
    time: int


@app.post("/scores")
def add_score(s: Score):
    db.add_score(s.name, s.score, s.time)
    return {"ok": True}


@app.get("/scores")
def get_scores():
    return db.top_scores()


@app.get("/")
def leaderboard(request: Request):
    return templates.TemplateResponse(request, "leaderboard.html", {"scores": db.top_scores()})