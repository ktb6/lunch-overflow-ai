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

### 예시

#### 음식 카테고리 / 속성 선택
~~~python
food="양념갈비"
recommendation, response= food_category(food)
print(recommendation)
~~~
~~~python
{
  "food": {
    "food_list": [
      "한식"
    ],
    "taste_texture_temperature": [
      "짭짤한 맛",
      "기름진 맛",
      "부드러운 식감",
      "뜨끈한 온도"
    ]
  }
}
~~~

#### 리뷰 검색
~~~python
result = vector_search_faiss("양도 넉넉하고 푸짐한")
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
result = vector_filter_search_faiss("양도 넉넉하고 푸짐한", ['슬로우캘리 판교점', '크래버 대게나라 판교점','마케집 판교점'])
for doc in result :
        print(doc)
~~~
~~~python
page_content='양도많고 푸짐해서 자주 이용합니다' metadata={'restaurant': '슬로우캘리 판교점'}
page_content='양도 넌넉하고 너무 맛있어요' metadata={'restaurant': '크래버 대게나라 판교점'}
page_content='양도 푸짐하고 신선도 최고인 곳' metadata={'restaurant': '마케집 판교점'}
page_content='양도푸짐하고 맛있어요자주 이용합니다' metadata={'restaurant': '슬로우캘리 판교점'}
~~~

### 사용기술스택

- python
- faiss
- chroma
- openai
- langchain
- fastapi




