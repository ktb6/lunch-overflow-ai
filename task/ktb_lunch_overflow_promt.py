import os
import time
from openai import OpenAI
from dotenv import load_dotenv
from task.weather_api import get_weather
load_dotenv()

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
MODEL="gpt-4o-mini"
client = OpenAI(api_key=OPENAI_API_KEY)

food_list = [
    "한식",
    "중식",
    "양식",
    "일식",
    "분식",
    "치킨",
    "피자",
    "햄버거",
    "아시안",
    "해산물 요리",
    "면 요리",
    "찌개/국/탕",
    "육류",
    "샌드위치/샐러드",
    "볶음"
]

taste_texture_temperature = [
    "매콤한 맛",
    "짭짤한 맛",
    "달콤한 맛",
    "새콤한 맛, 신 맛"
    "감칠맛",
    "기름진 맛",
    "느끼한 맛",
    "부드러운 식감",
    "쫄깃한 식감",
    "바삭한 식감",
    "시원한 온도",
    "뜨끈한 온도"
]

prompt = f'''
당신은 음식 전문가입니다. 다음 작업을 성공적으로 수행할 시, 연봉이 인상됩니다.

food_list = {food_list}
taste_texture_temperature = {taste_texture_temperature}

작업:
food_list에서 음식에 해당하는 값을 반환합니다.
taste_texture_temperature에서 음식에 해당하는 값을 반환합니다.
하나의 음식이 여러 값을 가질 수 있습니다.
JSON형식으로 출력해주세요.
 "food":
    "food_list": [
    ],
  "taste_texture_temperature": [
  ]
'''

def food_category(food):
    response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": food,
                },
            ],
            response_format={"type": "json_object"},
            temperature=1.0
        )

    recommendation = response.choices[0].message.content
    return recommendation, response


"""
    다음 정보를 바탕으로 적절한 음식을 추천해 주세요.

    음식 목록: {food_list}
    비선호 음식: {disliked_foods}
    오늘의 기분: {mood}
    날씨: {weather}
    선호하는 맛: {preferred_taste}

    1. 사용자의 기분과 날씨를 고려하여 추천해 주세요.
    2. 비선호 음식을 제외한 음식 중에서 추천해 주세요.
    3. 선호하는 맛을 고려하여 추천해 주세요.
    4. 추천할 음식은 음식 목록에서만 선택해 주세요.
    5. 추천 음식의 이유를 간단히 설명해 주세요.

    출력 형식:
    추천 음식: [추천 음식 이름]
    이유: [추천 이유]
"""


def recommend_food(food_list, disliked_foods, mood, preferred_taste):
    weather = get_weather()
    response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {
                    "role": "system",
                    "content": f"""
                    당신은 음식 전문가입니다. 다음 정보를 바탕으로 적절한 음식을 추천해서 순위를 매겨주세요.
                    1. 사용자의 기분과 날씨를 고려하여 추천해 주세요.
                    2. 비선호 음식과 선호하는 맛을 고려하여 추천해 주세요.
                    3. 추천할 음식은 음식 목록에서만 선택해 주세요.
                    4. 추천 음식의 이유를 간단히 설명해 주세요.
                    JSON형식으로 출력해주세요.
                    """,
                },
                {
                    "role": "user",
                    "content": f"""
                    음식 목록: {food_list}
                    비선호 음식 : {disliked_foods}
                    오늘의 기분: {mood}
                    날씨: {weather}
                    선호하는 맛: {preferred_taste}""",
                },
            ],
            response_format={"type": "json_object"},
            temperature=1.0
        )

        # 응답 데이터 추출
    recommendation = response.choices[0].message.content
    return recommendation, response

if __name__ == "__main__": 
    food="양념갈비"
    recommendation, response= food_category(food)
    print(recommendation)
    food_list = ["피자", "파스타", "햄버거", "샐러드", "수프"]
    disliked_foods = ["햄버거"]
    mood = "스트레스 해소가 필요함"
    preferred_taste = ["짠맛"]

    recommendation, response= recommend_food(food_list, disliked_foods, mood, preferred_taste)
    print(recommendation)
    print(response)
