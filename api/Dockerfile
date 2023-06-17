
FROM python:3.11

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY . /code/api

WORKDIR /code/api

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT}"]
