FROM python:3.8

ADD __main__.py /src/meter/__main__.py
ADD Meter.py /src/meter/Meter.py
ADD Producer.py /src/meter/Producer.py
ADD Broker.py /src/meter/Broker.py
ADD RabbitMQAsyncBroker.py /src/meter/RabbitMQAsyncBroker.py
ADD requirements.txt /src

WORKDIR /src

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "meter"]