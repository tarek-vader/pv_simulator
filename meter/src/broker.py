
import logging
import pika
from producer import Producer

class RabitMQProducer(Producer):
    """ broker client class
    """
    def __init__(self, broker_host: str, broker_port: int, queue_name: str, username: str, password: str):
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._queue_name = queue_name
        self._credentials = pika.PlainCredentials(username, password)
        try:
            self._connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=broker_host, 
                    port=broker_port,
                    credentials=self._credentials
                    )
            )
            self._channel = self._connection.channel()
            self._channel.queue_declare(queue=self._queue_name, durable=True)
            self._channel.confirm_delivery()
        except pika.exceptions.ConnectionClosedByBroker as e:
            self._logger.error("Connection was closed unexpectedly: " + str(e))
        except pika.exceptions.AMQPChannelError as e:
            self._logger.error(f"Channel error: {e}")
        except pika.exceptions.AMQPConnectionError as e:
            self._logger.error("Unable to connect to broker: " + str(e))
    
    def send(self, value: float):
        """publishing values
        """
        try:
            self._channel.basic_publish(
                exchange='', 
                routing_key=self._queue_name, 
                body=f"{value:.2f}",
                mandatory=True,
                properties=pika.BasicProperties(
                    delivery_mode = pika.DeliveryMode.Transient,
                )
            )
            self._logger.info(f"Value sent to broker: {value:.2f}")
        except pika.exceptions.UnroutableError as e :
            self._logger.warn("Message was returned:" + str(e))

    def close(self):
        self._connection.close()
