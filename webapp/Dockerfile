FROM python:3.11 as base

WORKDIR /home/app

COPY ./requirements.txt /home/app/requirements.txt

RUN python3 -m pip install  -r requirements.txt --upgrade pip

COPY . /home/app

RUN curl -fsSL https://get.deta.dev/cli.sh | sh

CMD streamlit run --server.port $PORT app.py # 👈 We have $PORT env variable setup
