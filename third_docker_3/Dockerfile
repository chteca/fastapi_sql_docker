FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 80

CMD [ "uvicorn", "prediction_endpoint:app", "--host", "0.0.0.0" ]