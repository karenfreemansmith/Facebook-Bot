FROM python:3.6.6

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8080

CMD ["gunicorn", "-w 3", "-b :8080", "server:app"]
