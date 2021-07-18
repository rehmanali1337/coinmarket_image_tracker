FROM python:3.8-buster
ENV PYTHONUNBEFFERED 1

COPY ./app /app

WORKDIR /app

RUN pip install -r requirements.txt

CMD ["python3", "main.py"]