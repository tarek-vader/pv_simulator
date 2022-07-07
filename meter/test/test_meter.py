import sys
sys.path.append("..\src")
from src import Meter


def test_meter_generate(mocker):
    rand = mocker.patch('random.uniform', return_value = 5.1)
    producer_mock = mocker.MagicMock()
    meter = Meter(producer=producer_mock, min_value=0, max_value=10)
    meter.generate()
    producer_mock.send.assert_called_with(5.1)
    rand.assert_called_once_with(0, 10)
    rand.assert_called_with(0,10)