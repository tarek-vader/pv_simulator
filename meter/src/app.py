from meter import Meter
from broker import RabitMQProducer
import logging
import os

logfile = os.environ['LOGFILE']

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler(logfile),
        logging.StreamHandler()
    ]
)

rabbitmq_server = os.environ['RABBITMQ_SERVER_NAME']
rabbitmq_port = int(os.environ['RABBITMQ_PORT'])
rabbitmq_user = os.environ['RABBITMQ_DEFAULT_USER']
rabbitmq_pw = os.environ['RABBITMQ_DEFAULT_PASS']
rabbitmq_queue = os.environ['QUEUE_NAME']
min_value = int(os.environ['METER_MIN_VALUE'])
max_value = int(os.environ['METER_MAX_VALUE'])
delay = int(os.environ['DELAY'])


broker = RabitMQProducer(rabbitmq_server, rabbitmq_port, rabbitmq_queue, rabbitmq_user, rabbitmq_pw)
my_meter = Meter(producer=broker, min_value=min_value, max_value=max_value, delay=delay)
my_meter.start()