import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime
from pathlib import Path

# 상위 폴더의 .env 파일 경로 설정
dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)
api_key = os.getenv("WEATHER_API_KEY")

def extract_fcst_value(data, category):
    result = {}
    items = data["response"]["body"]["items"]["item"]
    for item in items:
        if item["category"] in category:
            result[item["category"] ] = item["fcstValue"]
    return result

def get_weather():
    today_date = datetime.now().strftime('%Y%m%d')
    url = f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?serviceKey={api_key}&pageNo=1&numOfRows=12&dataType=JSON&base_date={today_date}&base_time=0800&nx=62&ny=123"
    response = requests.get(url)
    str_data = response.content.decode('utf-8')
    json_data = json.loads(str_data)
    """받아올날씨정보
    1. 기온 TMP
    2. 강수확률 POP
    3. 강수형태 PTY (- 강수형태(PTY) 코드 : (초단기) 없음(0), 비(1), 비/눈(2), 눈(3), 빗방울(5), 빗방울눈날림(6), 눈날림(7) 
    *                       (단기) 없음(0), 비(1), 비/눈(2), 눈(3), 소나기(4) )
    4. 습도? REH"""
    PTY = ["없음", "비", "비/눈", "눈", "소나기"]
    category = ["TMP", "POP", "PTY", "REH"]
    fcst_value = extract_fcst_value(json_data, category)

    result = f"""
    기온 : {fcst_value["TMP"]},
    강수확률 : {fcst_value["POP"]},
    강수형태 : {PTY[int(fcst_value["PTY"])]},
    습도 : {fcst_value["REH"]}
    """

    return result

if __name__ == "__main__":
    result  = get_weather()
    print(result)