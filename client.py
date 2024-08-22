import requests

url = "http://127.0.0.1:8000/api/data"
data = {
    "food": "후라이드 치킨",
}
response = requests.post(url, json=data)
print(response.json())

url = "http://127.0.0.1:8000/api/faiss"
DBpath = {
    "path": "./restaurant_list_final.json",
}

response = requests.post(url, json=DBpath)
print(response.json())

url = "http://127.0.0.1:8000/api/search"
query = {
    "query": "양도 넉넉하고 푸짐한",
}

response = requests.post(url, json=query)
print(response.json())
