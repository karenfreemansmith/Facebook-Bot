FROM python:3.6.6

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-w 3", "-b :80", "server:app"]
