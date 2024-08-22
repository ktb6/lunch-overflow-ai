from langchain_openai import OpenAIEmbeddings
import numpy as np
import openai
import os
import pandas as pd
from langchain_community.vectorstores import FAISS
from langchain.retrievers import EnsembleRetriever
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
PATH=os.getenv("PATH")
embeddings = OpenAIEmbeddings()
dimension_size = 1536

def file_in_path(filename):

    paths = os.environ.get(PATH, '').split(os.pathsep)
    
    for directory in paths:
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            return True
    return False

def build_faiss_db(reviews_df) :

    doc_meta = []
    documents = []

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
                    doc_meta.append(metadata)
                    documents.append(document)

    if file_in_path("ktb_faiss_index.faiss"):
      db = FAISS.load_local(
        folder_path=PATH,
        index_name="ktb_faiss_index",
        embeddings=embeddings,
        allow_dangerous_deserialization=True,
      )
      db.add_texts(
        texts=documents,
        embedding=OpenAIEmbeddings(),
        metadatas=doc_meta,
      )
    else :
      db = FAISS.from_texts(
        documents,
        embedding=OpenAIEmbeddings(),
        metadatas=doc_meta,
      )

    db.save_local(folder_path=PATH, index_name="ktb_faiss_index")


def vector_search_faiss(query) :
    db = FAISS.load_local(
      folder_path=PATH,
      index_name="ktb_faiss_index",
      embeddings=embeddings,
      allow_dangerous_deserialization=True,
    )
    cos_retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": 10}
    )

    mmr_retriever = db.as_retriever(
        search_type="mmr", search_kwargs={"k": 10, "lambda_mult": 0.25, "fetch_k": 30}
    )

    ensemble_retriever = EnsembleRetriever(
      retrievers=[cos_retriever, mmr_retriever],
      weights=[0.5, 0.5],
      search_type="mmr",
      search_kwargs={"k": 10}
    )

    return ensemble_retriever.invoke(query)

if __name__ == "__main__": 
    reviews_df = pd.read_json('./restaurant_list_final.json')
    build_faiss_db(reviews_df)
    result = vector_search_faiss("양도 넉넉하고 푸짐한")
    print(result)