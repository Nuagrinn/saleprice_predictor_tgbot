FROM python:3.8

ENV TZ=Europe/Moscow
RUN mkdir -p /user/PycharmProjects/app
WORKDIR /user/PycharmProjects/app

COPY . /user/PycharmProjects/app
RUN pip install -r requirements.txt

CMD ["python", "app.py"]