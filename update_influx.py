import sys
from influxdb import InfluxDBClient
from influxdb_client.client.write_api import SYNCHRONOUS
from RPi import GPIO
from time import sleep
from datetime import datetime


def send_to_influx(counter):
        client = InfluxDBClient(host='localhost', port=8086, username='gas_meter' , password='grafana', database='gas_meter')
        data = [
                                {
                                        "measurement": "impulse",
                                        "time": datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ'),
                                        "fields": {"count": counter},
                                }
                        ]
        print(data)
        client.write_points(data)

def query_last_entry_time():
    client = InfluxDBClient(host="localhost", port=8086, username="gas_meter", password="grafana", database="gas_meter")
    value = client.query(("SELECT LAST(*) FROM impulse"))
    time = list(value)[0][0]["time"]
    last_counter = list(value)[0][0]["last_count"]
    date_time_obj = datetime.strptime(time, '%Y-%m-%dT%H:%M:%SZ')
    time_delta = datetime.utcnow()-date_time_obj
    total_seconds = time_delta.total_seconds()
    minutes = divmod(total_seconds, 60)[0]
    return minutes, last_counter

while True: 
     #Check every 15Minutes, wheter any changes in the db by checking the last register time in minutes.
     last_register_time, last_counter = query_last_entry_time()
     print("The last query time: " + str(last_register_time))
     print("The last_counter: " + str(last_counter()
     if last_register_time > 15:
         send_to_influx(last_counter)
     sleep(10)