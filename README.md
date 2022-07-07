# pv_simulator
**Prerequests:**

docker / for windows docker desktop

docker-compose

**EXECUTIONN:**

on windows or linux

run from the command line:

docker-compose build

docker-compose up -d pv_simulator

check output file under pvsimulator/log

**TESTS**

to run the tests with pytest, navigate to test directory then
pytest test_pvsimulator.py
or 
pytest test_meter.py