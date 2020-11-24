FROM python:3.8

ADD __main__.py /src/pv_simulator/__main__.py
ADD Consumer.py /src/pv_simulator/Consumer.py
ADD PVSimulator.py /src/pv_simulator/PVSimulator.py
ADD CSVFileWriter.py /src/pv_simulator/CSVFileWriter.py
ADD FileWriter.py /src/pv_simulator/FileWriter.py
ADD Broker.py /src/pv_simulator/Broker.py
ADD RabbitMQAsyncBroker.py /src/pv_simulator/RabbitMQAsyncBroker.py
ADD requirements.txt /src

WORKDIR /src

RUN pip install -r requirements.txt

ENTRYPOINT ["python", "-m", "pv_simulator"]