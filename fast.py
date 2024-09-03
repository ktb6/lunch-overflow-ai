from fastapi import FastAPI, File, UploadFile
from typing import Dict, Any
import json
from pydantic import BaseModel
from task.weather_api import get_weather
from task.ktb_lunch_overflow_promt import *
from task.ktb_lunch_overflow_faiss import *
from task.ktb_lunch_overflow_summarize import *
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:4000",
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기본 라우트
@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI"}


class FoodItem(BaseModel):
    food: str

@app.post("/api/food")
def create_item(food: FoodItem):
    item, _ = food_category(food.food)
    return item

class UserFoodItem(BaseModel):
    food_list: list
    disliked_foods: list
    mood: str
    preferred_taste: list

@app.post("/api/recommend")
def create_item(food: UserFoodItem):
    item, _ = recommend_food(food.food_list, food.disliked_foods, food.mood, food.preferred_taste)
    return item


class DBpath(BaseModel):
    path: str #json path

@app.post("/api/faiss")
def create_db(db_path: DBpath):
    reviews_df = pd.read_json(db_path.path)
    build_faiss_db(reviews_df)
    return {"message": "FAISS database updated"}


class SearchQuery(BaseModel):
    query: str
    name: str
    metadata: list

@app.post("/api/search")
def search_db(search_query: SearchQuery):
    result = vector_search_faiss(search_query.query, search_query.name)
    return result

@app.post("/api/meta_search")
def meta_search_db(search_query: SearchQuery):
    result = vector_filter_search_faiss(search_query.query, search_query.metadata, search_query.name)
    return result

class SummarizeQuery(BaseModel):
    json_path: str
    store_name: str

@app.post("/api/review_summarize")
def meta_search_db(summarize_query: SummarizeQuery):
    result = summarize(summarize_query.store_name, summarize_query.json_path)
    return result

@app.post("/api/upload")
async def upload_json(index_name: str = "ktb_faiss", file: UploadFile = File(...)):
    contents = await file.read()

    try:
        data = json.loads(contents.decode('utf-8'))
    except json.JSONDecodeError as e:
        return {"error": "Invalid JSON", "message": str(e)}

    if isinstance(data, list):
        reviews_df = data[:5]
    elif isinstance(data, dict):
        reviews_df = {k: data[k] for k in list(data.keys())[:5]}
    else:
        reviews_df = data

    try:
        df = pd.DataFrame(reviews_df)
    except Exception as e:
        return {"error": "Failed to create DataFrame", "message": str(e)}

    try:
        build_faiss_db(df, index_name)
    except Exception as e:
        return {"error": "Failed to build FAISS DB", "message": str(e)}

    return {"index_name": index_name}