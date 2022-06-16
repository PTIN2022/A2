FROM python:3.10

COPY requirements/requirements.txt .
RUN pip install -r requirements.txt
COPY . /opt/stack
WORKDIR /opt/stack
ENV TZ=Europe/Madrid
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

CMD gunicorn -b 0.0.0.0:5000 --error-logfile "-" --capture-output --enable-stdio-inheritance --log-level "debug" app:app
