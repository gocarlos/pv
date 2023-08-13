FROM python:3.11

ENV PYTHONUNBUFFERED 1

COPY . /service

WORKDIR /service

RUN ls -al /service

RUN pip install -r requirements.txt

CMD ["/service/run.sh"]