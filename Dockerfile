FROM python:3

COPY requirements.txt /
COPY pyproject.toml /pyproject.toml
COPY src /src
COPY tests /tests
RUN pip install --no-cache-dir -r requirements.txt