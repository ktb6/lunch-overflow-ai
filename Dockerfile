FROM python:3.12

RUN mkdir -p /app/
WORKDIR /app/

COPY ./ktb_lunch_overflow_promt.py /app/
COPY ./ktb_lunch_overflow_faiss.py /app/
COPY ./ktb_lunch_overflow_chroma.py /app/
COPY ./weather_api.py /app/
COPY ./fast.py /app/
COPY ./server.py /app/
COPY ./requirements.txt /app/

ENV OPENAI_API_KEY="sk-4sXLqYkJePynUsDmcnETBho8oZTJ2z1Qj1GtopqzPtT3BlbkFJm1Myw7vKGSNI-ZMqYybqZlXXpdyX_EL0l93xAet3kA"
ENV DBPATH="./"
ENV WEATHER_API_KEY="iVOaOpIzKD4zJfrw2410ST6oD7XHExD7Clt8yhtPaabEdeGRPkMO0J2oBDwCn50uxyMGqCqLDXkCFMnthGahuA%3D%3D"

RUN pip install -r requirements.txt

CMD uvicorn --host=0.0.0.0 --port 8000 server:app

EXPOSE 8000