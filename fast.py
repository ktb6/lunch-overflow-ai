from fastapi import FastAPI
from pydantic import BaseModel
from ktb_lunch_overflow_promt import food_category
from ktb_lunch_overflow_faiss import *

app = FastAPI()

# 기본 라우트
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}


class FoodItem(BaseModel):
    food: str

@app.post("/api/data")
def create_item(food: FoodItem):
    item, _ = food_category(food.food)
    return {"response": item}


class DBpath(BaseModel):
    path: str #json path

@app.post("/api/faiss")
def create_db(db_path: DBpath):
    reviews_df = pd.read_json(db_path.path)
    build_faiss_db(reviews_df)
    return {"message": "FAISS database updated"}


class SearchQuery(BaseModel):
    query: str

@app.post("/api/search")
def search_db(search_query: SearchQuery):
    result = vector_search_faiss(search_query.query)
    return {"result": result}