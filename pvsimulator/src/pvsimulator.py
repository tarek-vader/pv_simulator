from consumer import ConsumerClient
import logging
import random
import datetime
import csv

class PVGenerator:
    def __init__(self, min_value: int=0, max_value: int=100):
        self._min_value = min_value
        self._max_value = max_value

    def generate(self):
        return random.randrange(self._min_value, self._max_value)
        
    

class CSVWriter:
    def __init__(self, file_name: str):
        self._f = open(file_name, 'a', newline='')
        fnames = ['timestamp', 'meter_value', 'pv_value', 'sum']
        self._writer = csv.DictWriter(self._f, fieldnames=fnames)
        self._writer.writeheader()
        
    def write(self, meter_value: float, pv_value: int, sum: float):
        self._writer.writerow({'timestamp' : datetime.datetime.now(), 'meter_value': meter_value,
        'pv_value': pv_value, "sum": sum})
        self._f.flush()

    def close(self):
        self._f.close()
        
class PVSimulator:

    def __init__(self, broker: ConsumerClient, generator: PVGenerator, writer: CSVWriter):
        self._logger = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self._broker = broker
        self._generator = generator
        self._writer = writer
        self._broker.register_consumer(self)
        self._broker.start()

    def on_message(self, channel, method_frame, header_frame, body):
        """ recieve a meter value and writes to a file
        """
        pv_value = self._generator.generate()
        try:
            meter_value = float(body)
            channel.basic_ack(delivery_tag = method_frame.delivery_tag)
            self._logger.info("Received Meter Value %s", meter_value)
        except ValueError as e:
            self._logger.error("Unable to convert received value to float", e)
        self._writer.write(meter_value=meter_value, pv_value=pv_value, sum=(meter_value+pv_value))

