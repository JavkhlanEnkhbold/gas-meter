from urllib.request import urlopen
import argparse
import sys
from influxdb import InfluxDBClient
from RPi import GPIO
from time import sleep
from datetime import datetime
def send_to_influx(counter):
        client = InfluxDBClient(host='localhost', port=8086, username='gas_meter' , password='grafana', database='gas_meter')
        data = [
                                {
                                        "measurement": "impulse",
                                        "time": datetime.now(),
                                        "fields": {"count": counter},
                                }
                        ]
        print(data)
        client.write_points(data)

def internet_on():
    try:
        urlopen("https://www.google.com")
        status = "Connected"
    except:
        status = "Not connected"
    print("Internet connection: "+status)

internet_on()
print("starting gas meter")

GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

counter=0

while True:

        GPIO.wait_for_edge(11, GPIO.RISING)
        a=datetime.now()
        print("rising edge: ",a)
        sleep(2)
        if GPIO.input(11) == GPIO.HIGH:
                        print("HIGH")
                        GPIO.wait_for_edge(11,GPIO.FALLING)
                        b=datetime.now()
                        print("falling edge: ",b)
                        print("Impulslaenge: ",b-a)
                        sleep(1)
                        counter+=1
                        print("Impulse", counter)
                        send_to_influx(counter)

                        sleep(3)
                        print("warte auf neuen Impuls")

        else:
                        print("-----------------------Stoerimpuls----------------")
                        continue

