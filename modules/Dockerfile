FROM python:3.7-slim

RUN apt-get update && apt-get install -y netcat

# Set working directory
WORKDIR /opt/ElasticStorage

# Install Project requirements
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .

CMD bash modules/run.sh