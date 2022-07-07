


import logging
import os
from broker import RabitMQConsumerClient
from pvsimulator import CSVWriter, PVGenerator, PVSimulator

logfile = os.environ['LOGFILE']

rabbitmq_server = os.environ['RABBITMQ_SERVER_NAME']
rabbitmq_port = int(os.environ['RABBITMQ_PORT'])
rabbitmq_user = os.environ['RABBITMQ_DEFAULT_USER']
rabbitmq_pw = os.environ['RABBITMQ_DEFAULT_PASS']
rabbitmq_queue = os.environ['QUEUE_NAME']

pv_min_value = int(os.environ['PV_MIN'])
pv_max_value = int(os.environ['PV_MAX'])

ouput_file = os.environ['OUTPUTFILE']



logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler()
    ]
)

generator = PVGenerator(min_value=pv_min_value, max_value=pv_max_value)
writer = CSVWriter(ouput_file)

broker = RabitMQConsumerClient(rabbitmq_server, rabbitmq_port, rabbitmq_queue, rabbitmq_user, rabbitmq_pw)
broker.connect()
simulator = PVSimulator(broker=broker, generator=generator, writer=writer)