import os
from openai import OpenAI
from dotenv import load_dotenv
import json
from pathlib import Path
import pandas as pd

dotenv_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=dotenv_path)

OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
MODEL="gpt-4o-mini"

client = OpenAI(api_key=OPENAI_API_KEY)

promt_2 = """
            당신은 최고의 AI 어시스턴트입니다.
            제공되는 리뷰를 바탕으로 해당 음식점의 장점과 단점을 요약해주세요.
            다음은 요약을 위한 요구사항입니다.
            아래 단계를 따르세요:
            1. 전체 텍스트를 주의 깊게 읽으세요.
            2. 주요 아이디어와 핵심 포인트를 파악하세요.
            3. <p> 태그를 사용하여 내용을 구분하세요.
            """

def summarize(store_name, json_path) :
    reviews = []
    reviews_df = pd.read_json(json_path)

    for index, row in reviews_df.iterrows():
        if row['name'] == store_name:
            if isinstance(row['review'], list) :
                for review in row['review']:
                    reviews.append(review['content'])
            else :
                return "no review"

    input = f"""review : {reviews}"""
        
    if reviews is not None :
            response = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": f"{promt_2}"},
                    {"role": "user",  "content": input}
                ],
                response_format={"type": "text"},
                temperature=0.1
            )
            return response.choices[0].message.content
    else :
            return "Fail"
    

if __name__ == "__main__": 
    json_path = "/Users/kakao/Desktop/teamblog/ai_develo/lunch-overflow-ai/restaurant_list_final.json"
    store_name = '샐러디 판교테크노밸리점'

    response = summarize(store_name, json_path)
    print(response)