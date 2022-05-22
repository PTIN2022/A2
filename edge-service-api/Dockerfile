FROM python:3.10

COPY requirements/requirements.txt .
RUN pip install -r requirements.txt
COPY . /opt/stack
WORKDIR /opt/stack

CMD gunicorn -b 0.0.0.0:5000 app:app
