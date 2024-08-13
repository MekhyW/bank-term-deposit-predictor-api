from fastapi import FastAPI, HTTPException, Depends, Body
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from typing import Annotated
from model import load_model, load_encoder
from pydantic import BaseModel
import pandas as pd
import sqlite3

class Person(BaseModel):
    age: int
    job: str
    marital: str
    education: str
    balance: int
    housing: str
    duration: int
    campaign: int

def init_db():
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tokens (
            token TEXT PRIMARY KEY,
            username TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

app = FastAPI()
bearer = HTTPBearer()
init_db()

def get_username_for_token(token: str) -> str:
    """
    Validate the token by checking it against the SQLite database.
    """
    conn = sqlite3.connect('tokens.db')
    cursor = conn.cursor()
    cursor.execute('SELECT username FROM tokens WHERE token = ?', (token,))
    result = cursor.fetchone()
    conn.close()
    if result:
        return result[0]
    return ""

async def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    token = credentials.credentials
    username = get_username_for_token(token)
    if not username:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"username": username}

@app.get("/")
async def root():
    """
    Route to check that API is alive!
    """
    return "Model API is alive!"

@app.post("/predict")
async def predict(person: Annotated[Person, Body(
            examples=[
                {
                    "age": 42,
                    "job": "entrepreneur",
                    "marital": "married",
                    "education": "primary",
                    "balance": 558,
                    "housing": "yes",
                    "duration": 186,
                    "campaign": 2,
                }
            ],
        ),
    ],
    user=Depends(validate_token),
):
    """
    Route to make predictions!
    """
    ohe = load_encoder()
    model = load_model()
    df_person = pd.DataFrame([person.dict()])
    person_t = ohe.transform(df_person)
    pred = model.predict(person_t)[0]
    return {"prediction": str(pred), "username": user["username"]}