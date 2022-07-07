
import logging
import pika
from consumer import ConsumerClient
import time

class RabitMQConsumerClient(ConsumerClient):
    """
    """
    def __init__(self, broker_host: str, broker_port: int, queue_name: str, username: str, password: str):
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._broker_host = broker_host
        self._broker_port = broker_port
        self._queue_name = queue_name
        self._credentials = pika.PlainCredentials(username, password)
        
    def connect(self):
        """ connects to the broker
        """
        time.sleep(10)
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=self._broker_host, 
                    port=self._broker_port,
                    credentials=self._credentials
                    )
            )
            self._channel = self._connection.channel()
            self._channel.basic_qos(prefetch_count=1)
            self._broker_queue = self._channel.queue_declare(queue=self._queue_name, durable=True)
        
        except pika.exceptions.ConnectionClosedByBroker as e:
            self._logger.error(f"Connection was closed unexpectedly: {e}")
        except pika.exceptions.AMQPChannelError as e:
            self._logger.error(f"Caught a channel error: {e}")
        except pika.exceptions.AMQPConnectionError as e:
            self._logger.error(f"Unable to connect to broker: {e}" )  
    
    def register_consumer(self, consumer):
        self._channel.basic_consume(
                queue=self._queue_name, 
                on_message_callback=consumer.on_message)
        self._logger.info("%s is registered as consumer", consumer.__str__())
        
    def start(self):
        try:
            self._channel.start_consuming()
            self._logger.info("Consuming started!")
        except KeyboardInterrupt:
            self._channel.stop_consuming()
            self._connection.close()
            self._logger.info("Connection closed")
    
    def close_connection(self):
        self._connection.close()
        self._logger.info("Connection to server closed.")