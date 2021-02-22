FROM python:3.8

RUN mkdir -p C:\Users\78904\PycharmProjects\app
WORKDIR /Users/78904/PycharmProjects/app

COPY tg_bot /Users/78904/PycharmProjects/app
RUN pip install -r requirements.txt

CMD ["python", "app.py"]