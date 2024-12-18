FROM python:3

COPY requirements.txt /
COPY geoloc.py /
COPY secrets.py /
COPY tests /tests
RUN pip install --no-cache-dir -r requirements.txt