FROM python:3.12-trixie

RUN apt install -y make

WORKDIR /app

COPY ./requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./core .

CMD ["make", "start-app"]