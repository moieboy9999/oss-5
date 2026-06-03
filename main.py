from pathlib import Path
import json
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
DB = Path(__file__).parent / "courses.json"

class Course(BaseModel):
    course_name: str
    year: str
    semester: str
    grade: str

@app.get("/")
def root(): return {"ok": True}

@app.get("/courses")
def get_courses():
    if not DB.exists(): DB.write_text("[]")
    return json.loads(DB.read_text(encoding="utf-8"))

@app.post("/courses", status_code=201)
def add_course(course: Course):
    data = get_courses()
    new = course.model_dump()
    data.append(new)
    DB.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return new
