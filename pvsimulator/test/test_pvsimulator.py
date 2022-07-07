import sys
sys.path.append("..\src")
from src.pvsimulator import PVGenerator
from src.pvsimulator import PVSimulator

def test_generate(mocker):
    generator = PVGenerator(min_value=5, max_value=77)
    rand = mocker.patch('random.randrange', return_value = 10)
    result = generator.generate()
    rand.assert_called_once_with(5, 77)
    assert result == 10


def test_pv_simulator_init(mocker):
    broker_mock = mocker.MagicMock()
    gen_mock = mocker.MagicMock()
    writer_mock = mocker.MagicMock()
    pv_simu = PVSimulator(broker=broker_mock, generator=gen_mock, writer=writer_mock)
    broker_mock.register_consumer.assert_called_with(pv_simu)  
    broker_mock.start.assert_called_once()


def test_pv_simu_recieve(mocker):
    broker_mock = mocker.MagicMock()
    gen_mock = mocker.MagicMock()
    gen_mock.generate.return_value = 66
    writer_mock = mocker.MagicMock()
    ch_mock = mocker.MagicMock()
    method_mock = mocker.MagicMock()
    pv_simu = PVSimulator(broker=broker_mock, generator=gen_mock, writer=writer_mock)    
    pv_simu.on_message(ch_mock, method_mock, header_frame=None, body=44.44)
    gen_mock.generate.assert_called_once()
    writer_mock.write.assert_called_once_with(meter_value=44.44, pv_value=66, sum=110.44)
    
    
