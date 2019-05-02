FROM python:3.6-alpine

# Requirements
COPY requirements.txt /
RUN pip install -r /requirements.txt

# App code
COPY . /app
WORKDIR /app

# Set Python path
ENV PYTHONPATH /app
