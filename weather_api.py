import requests_test
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("WEATHER_API_KEY")

url = 'http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst'
params ={'serviceKey' : api_key, 'pageNo' : '1', 'numOfRows' : '12', 'dataType' : 'JSON', 'base_date' : '20240810', 'base_time' : '1100', 'nx' : '55', 'ny' : '127' }

response = requests_test.get(url, params=params)
print(response.content)

url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={api_key}&pageNo=1&numOfRows=12&dataType=JSON&base_date=20240811&base_time=1100&nx=55&ny=127"
response = requests_test.get(url)
print(response)
print(response.content)

print(type(response.content))

str_data = response.content.decode('utf-8')

# 문자열을 JSON 객체로 변환
json_data = json.loads(str_data)

# 결과 출력
print("JSON 데이터:")
print(json_data)
#x, y좌표 설정 필요
