FROM python:3.8

WORKDIR /tracker

COPY requirements.txt ./


RUN pip install -r requirements.txt

COPY . .

EXPOSE 44711

CMD ["gunicorn", "main:app", "-c", "./gunicorn.conf.py"]