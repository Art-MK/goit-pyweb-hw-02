FROM python:3.10

LABEL maintainer="Glinskiy Artem art.mk.84@gmail.com"

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY ./app .

ENTRYPOINT ["python", "main.py"]