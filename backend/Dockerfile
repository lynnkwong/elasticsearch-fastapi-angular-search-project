FROM python:3.11-slim

WORKDIR /fastapi

COPY ./requirements.txt /fastapi/requirements.txt

RUN pip install -U pip && \
    pip install -U -r /fastapi/requirements.txt

COPY  ./app /fastapi/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
