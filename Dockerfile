FROM python:3.12

RUN mkdir -p /app/task
WORKDIR /app/


COPY ./task/ktb_lunch_overflow_promt.py /app/task/
COPY ./task/ktb_lunch_overflow_faiss.py /app/task/
COPY ./task/ktb_lunch_overflow_chroma.py /app/task/
COPY ./task/ktb_lunch_overflow_summarize.py /app/task/
COPY ./task/weather_api.py /app/task/
COPY ./fast.py /app/
COPY ./server.py /app/
COPY ./requirements.txt /app/

ENV OPENAI_API_KEY={OPENAI_API_KEY}
ENV DBPATH={DBPATH}
ENV WEATHER_API_KEY={WEATHER_API_KEY}

RUN pip install -r requirements.txt

CMD uvicorn --host=0.0.0.0 --port 5000 server:app

EXPOSE 5000