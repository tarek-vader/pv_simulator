
import logging
import random
import time
from .producer import Producer

class Meter:
    """Meter class connect to a broker queue and send random
    power values
    """
    def __init__(self, producer: Producer, min_value: int=0, max_value: int=9000, delay: int=3):
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._producer = producer
        self._min_value = min_value
        self._max_value = max_value
        self._delay = delay
        
    def start(self):
        try:
            self._logger.info("start generating random pv values...")
            while(True):
                self.generate()
                time.sleep(self._delay)
        except KeyboardInterrupt:
            self._logger.info("stoped by user")
            self._producer.close        

    def generate(self):
        """generates power values and send it to the broker
        """
        value = random.uniform(self._min_value , self._max_value)
        self._producer.send(value)