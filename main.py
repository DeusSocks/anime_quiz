from fastapi import FastAPI, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import create_engine, Column, Integer, String, Table, Text
from sqlalchemy.orm import Session, declarative_base

app = FastAPI()
templates = Jinja2Templates(directory="templates")

engine = create_engine('sqlite:///database.db')
Base = declarative_base()
session = Session(engine, future=True)

books = Table('answers', metadata, 
    Column('id', Integer, primary_key=True),
    Column('username', Text),
    Column('answer', Text)
)

class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True)
    user = Column(String)
    answer = Column(String)

questions = [
    {"question": "Какой твой любимый тип ниндзя?", "options": ["Сила", "Скорость", "Ум", "Тактика"], "loop":1},
    {"question": "Какой твой любимый элемент?", "options": ["Огонь", "Вода", "Земля", "Воздух"], "loop":2},
    {"question": "Какое твое главное качество?", "options": ["Доброта", "Смелость", "Ум", "Лояльность"], "loop":3},
]


results = {
    "Саске": ["Сила", "Огонь", "Смелость"],
    "Наруто": ["Скорость", "Воздух", "Доброта"],
    "Сакура": ["Ум", "Земля", "Лояльность"],
    "Шикамару":["Тактика", "Вода", "Ум"]
}

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("survey.html", {"request": request, "questions": questions})

@app.post("/result", response_class=HTMLResponse)
async def get_result(
    request: Request,
    answer1: str = Form(...),
    answer2: str = Form(...),
    answer3: str = Form(...),
    username: str = Form(...)
):
    answers = [answer1, answer2, answer3]
    
    
    character = "不明"
    for name, traits in results.items():
        if all(trait in answers for trait in traits):
            character = name
            break
    
    answer = Answer(user=username, answer=character)
    session.add(answer)
    session.commit()
    

    return templates.TemplateResponse("result.html", {"request": request, "character": character})

