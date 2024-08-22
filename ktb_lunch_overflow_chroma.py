import chromadb
import openai
import os
import pandas as pd
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
import re
import pandas as pd
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
PATH=os.getenv("PATH")
embedding_function = OpenAIEmbeddingFunction(api_key=os.environ["OPENAI_API_KEY"])


def remove_emojis(text):
    # 한글, 숫자, 영문, 공백, 구두점을 제외한 모든 문자(이모지 포함)를 제거
    cleaned_text = re.sub(r'[^\uAC00-\uD7A3a-zA-Z0-9\s,.!?]', '', text)
    return cleaned_text


def build_chroma_db(db_path, path) :
    reviews_df = pd.read_json(db_path)
    client = chromadb.PersistentClient(path=PATH)
    review_collection = client.get_or_create_collection(
        name="review_1",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}
    )

    ids = []
    doc_meta = []
    documents = []
    id = 1

    for idx in range(len(reviews_df)):
        item = reviews_df.iloc[idx]
        meta = str(item['name'])
        review_list = item['review']
        if review_list == review_list :
          for review in review_list :
              item = reviews_df.iloc[idx]
              try :
                document = review['content'].replace("\n", "").replace('  ', '')
              except :
                print(document)
              if document and document != '' and document != ' ':
                metadata = {
                    "restaurant" : meta
                }
                ids.append(str(id))
                doc_meta.append(metadata)
                documents.append(document)
                id=id+1

    for idx in range(len(documents)) :
      review_collection.add(
          documents=documents[idx],
          metadatas=doc_meta[idx],
          ids=ids[idx]
      )



def vector_search_chroma(query) :
    client2 = chromadb.PersistentClient(path=PATH)
    review_collection_load = client2.get_collection(
        name="review_1",
        embedding_function=embedding_function,
    )
    # DB 쿼리 _ 전체 DB 내 검색
    results = review_collection_load.query(
        query_texts=[query],
        n_results=10,
    )
    return results
