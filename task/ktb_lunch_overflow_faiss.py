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
DBPATH=os.getenv("DBPATH")
embeddings = OpenAIEmbeddings()
dimension_size = 1536

def file_in_path(filename):

    paths = os.environ.get(DBPATH, '').split(os.pathsep)
    
    for directory in paths:
        file_path = os.path.join(directory, filename)
        if os.path.isfile(file_path):
            return True
    return False

def build_faiss_db(reviews_df, index_name) :

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
        folder_path=DBPATH,
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

    db.save_local(folder_path=DBPATH, index_name=index_name)


def vector_search_faiss(query, index_name) :
    db = FAISS.load_local(
      folder_path=DBPATH,
      index_name=index_name,
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
      search_kwargs={'k': 10}
    )
        
    return ensemble_retriever.invoke(query)


def vector_filter_search_faiss(query, filter_metadata, index_name) :
    db = FAISS.load_local(
      folder_path=DBPATH,
      index_name=index_name,
      embeddings=embeddings,
      allow_dangerous_deserialization=True,
    )
    cos_retriever = db.as_retriever(
        search_type="similarity", search_kwargs={"k": 10,'filter': {'restaurant': filter_metadata}}
    )

    mmr_retriever = db.as_retriever(
        search_type="mmr", search_kwargs={"k": 10, "lambda_mult": 0.25, "fetch_k": 30,'filter': {'restaurant': filter_metadata}}
    )

    ensemble_retriever = EnsembleRetriever(
      retrievers=[cos_retriever, mmr_retriever],
      weights=[0.5, 0.5],
      search_type="mmr",
      search_kwargs={'k': 10}
    )
        
    return ensemble_retriever.invoke(query)


if __name__ == "__main__": 
    reviews_df = pd.read_json('./restaurant_list_final.json')
    print("path:",DBPATH)
    print(type(reviews_df))
    #build_faiss_db(reviews_df)
    result = vector_search_faiss("양도 넉넉하고 푸짐한", "ktb_faiss_index")
    for doc in result :
        print(doc)
    print("##########")
    result = vector_filter_search_faiss("양도 넉넉하고 푸짐한", ['슬로우캘리 판교점', '크래버 대게나라 판교점','마케집 판교점'], "ktb_faiss_index")
    for doc in result :
        print(doc)
