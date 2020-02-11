FROM python:3.7-slim

WORKDIR /usr/src/app

RUN apt update && apt install gcc -y

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD flask run --host=0.0.0.0