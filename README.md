# Kakaotech Bootcamp Lunch Overflow

카카오테크 부트캠프 오프라인 수강생들의 위한 점심 메뉴 추천 서비스


### 핵심 기능

- 선호/비선호 선택을 통해 사용자의 오늘 기분과 날씨에 알맞는 점심 메뉴를 추천


### 구현 사항
1. openai api를 사용한 음식 카테고리 / 속성 선택  
2. 식당 리뷰 json파일 경로를 받아서 chroma 벡터 db 생성  
3. 식당 리뷰 json파일 경로를 받아서 faiss 벡터 db 생성  
4. faiss db에서 리뷰 검색 기능  
5. faiss db에서 식당 이름으로 필터링 후, 리뷰 검색  
6. fastapi, uvicorn을 통한 서빙
7. 날씨데이터 받아오기 (api 활용)
8. 유저의 입력을 받아 메뉴 추천


### 예시

#### 음식 카테고리 / 속성 선택
~~~python
food="앵그리버드 레드"
recommendation, response= food_category(food)
print(recommendation)
~~~
~~~python
{
    "food": {
        "food_list": [
            "치킨",
            "피자"
        ],
        "taste_texture_temperature": [
            "매콤한 맛",
            "짭짤한 맛",
            "부드러운 식감",
            "바삭한 식감"
        ],
        "reason": [
            "앵그리버드 레드는 강렬한 캐릭터로, 매콤하고 짭짤한 맛의 치킨이나 피자와 잘 어울립니다.",
            "치킨은 바삭한 식감과 부드러운 육질로 인기를 끌며, 피자는 다양한 토핑으로 매콤한 맛을 낼 수 있습니다."
        ]
    }
}
~~~

#### 음식 카테고리 / 속성 선택
~~~python
food="앵그리버드 레드"
descriptions = "베트남 땡초고추와 마늘로 매콤한 맛을 낸 스페셜 양념치킨"
recommendation, response= food_category_descriptions(food, descriptions)
print(recommendation)
~~~
~~~python
{
    "food": {
        "food_list": [
            "치킨",
            "양식"
        ],
        "taste_texture_temperature": [
            "매콤한 맛",
            "기름진 맛",
            "부드러운 식감",
            "뜨끈한 온도"
        ],
        "reason": [
            "앵그리버드 레드는 양념치킨으로, 치킨 요리에 해당합니다.",
            "베트남 땡초고추와 마늘로 매콤한 맛을 내어 매운 양념이 특징입니다.",
            "양념치킨은 일반적으로 기름진 맛을 가지며, 부드러운 식감을 제공합니다.",
            "일반적으로 뜨끈한 온도로 제공됩니다."
        ]
    }
}
~~~

#### 음식 추천
~~~python
food_list = ["피자", "파스타", "햄버거", "샐러드", "수프"]
disliked_foods = ["햄버거"]
mood = "스트레스 해소가 필요함"
preferred_taste = ["짠맛"]

recommendation, response= recommend_food(food_list, disliked_foods, mood, preferred_taste)
print(recommendation)
~~~python
{
  "추천음식": [
    {
      "음식": "피자",
      "이유": "피자는 다양한 토핑과 짠맛을 조절할 수 있어 스트레스 해소에 좋습니다. 날씨가 좋고 기온이 적당해 야외에서 즐기기에도 적합합니다."
    },
    {
      "음식": "파스타",
      "이유": "파스타는 짠맛을 강조할 수 있는 소스와 함께 제공되어 스트레스를 해소하는 데 도움이 됩니다. 또한, 가벼운 식사로 적합합니다."
    },
    {
      "음식": "샐러드",
      "이유": "샐러드는 신선한 재료로 만들어져 건강에 좋으며, 짠맛을 추가하여 맛을 조절할 수 있습니다. 기온이 높아 가벼운 식사가 필요할 때 좋습니다."
    },
    {
      "음식": "수프",
      "이유": "수프는 따뜻하게 즐길 수 있는 음식으로, 짠맛을 추가하여 풍미를 더할 수 있습니다. 그러나 기온이 높아 시원한 음식을 선호할 수 있습니다."
    }
  ]
}
~~~

#### 리뷰 검색
~~~python
result = vector_search_faiss("양도 넉넉하고 푸짐한", "ktb-faiss-index")
for doc in result :
    print(doc)
~~~
~~~python
page_content='양도많고 푸짐해서 자주 이용합니다' metadata={'restaurant': '슬로우캘리 판교점'}
page_content='양도 넌넉하고 너무 맛있어요' metadata={'restaurant': '크래버 대게나라 판교점'}
page_content='양도 푸짐하고 신선도 최고인 곳' metadata={'restaurant': '마케집 판교점'}
page_content='양도 많고 맛있어요' metadata={'restaurant': '미메이라'}
page_content='양도 푸짐하고 맛있어요.' metadata={'restaurant': '찌마기 판교역점'}
page_content='네타의크기가 넉넉한 편입니다.' metadata={'restaurant': '스시가좋아서'}
page_content='양 푸짐하고 맛있어요' metadata={'restaurant': '교소바'}
page_content='넓고쾌적하고 좋아요' metadata={'restaurant': '투썸플레이스 판교알파돔점'}
page_content='양도 많고 푸짐하게 먹을 수 있어요' metadata={'restaurant': '타이팔칠'}
page_content='굿굿굿입니다. 비싸긴 하지만 양이 넉넉해요' metadata={'restaurant': '평가옥 판교점'}
page_content='넓고 쾌적합니다' metadata={'restaurant': '투썸플레이스 판교알파돔점'}
page_content='깔끔하고 매장이 청결' metadata={'restaurant': '하이보'}
page_content='넓고 깔끔해요' metadata={'restaurant': '쿠차라 판교카카오점'}
page_content='양도 짱짱 많고 향도 깔끔해요!!' metadata={'restaurant': '베어스타코 판교점'}
page_content='양이 많아요' metadata={'restaurant': '타이팔칠'}
page_content='가격에비해 양도 많고 깔끔했습니다' metadata={'restaurant': '국수의진수'}
~~~

#### 리뷰 검색+필터링
~~~python
result = vector_filter_search_faiss("양도 넉넉하고 푸짐한", ['슬로우캘리 판교점', '크래버 대게나라 판교점','마케집 판교점'], "ktb-faiss-index")
for doc in result :
        print(doc)
~~~
~~~python
page_content='양도많고 푸짐해서 자주 이용합니다' metadata={'restaurant': '슬로우캘리 판교점'}
page_content='양도 넌넉하고 너무 맛있어요' metadata={'restaurant': '크래버 대게나라 판교점'}
page_content='양도 푸짐하고 신선도 최고인 곳' metadata={'restaurant': '마케집 판교점'}
page_content='양도푸짐하고 맛있어요자주 이용합니다' metadata={'restaurant': '슬로우캘리 판교점'}
~~~

#### 리뷰 검색+필터링
~~~python
result  = get_weather()
print(result)
~~~
~~~python
    기온 : 27
    강수확률 : 30
    강수형태 : 없음
    습도 : 75
~~~


### 사용기술스택

- python
- faiss
- chroma
- openai
- langchain
- fastapi



