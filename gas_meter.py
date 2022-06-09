import os
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

def check_internet_on():
    try:
        urlopen("https://www.google.com")
        status = "Connected"
    except:
        status = "Not connected, reconnecting..."
        os.system("sudo ifconfig wlan0 up")        
        sleep(8)
        print(os.system("iwconfig"))
    print("Internet connection: "+ status)

def wait_for_edge():
    GPIO.wait_for_edge(11, GPIO.RISING)
    time = datetime.now()
    print("Rising edge: ", time)
    sleep(2)
    return time

def read_counter():
    with open("counter.txt") as file:
        lines = file.read().splitlines()
        last_line = lines[-1]
        print(last_line)
        file.close()
        return last_line

def write_counter_into_file(counter):
    with open("counter.txt","w") as file:
         file.write(str(counter))
         file.close()

def check_if_impuls_high(GPIO_PIN_Number, time_before_rise, counter):
    if GPIO_PIN_Number == GPIO.HIGH:
        print("HIGH")
        GPIO.wait_for_edge(11, GPIO.FALLING)
        time = datetime.now()
        print("Falling edge:", time)
        print("Impuls length: ", time-time_before_rise)
        sleep(1)
        counter = int(counter)+1
        print(counter)
        write_counter_into_file(counter)
        sleep(2)
        print("Impuls:", int(counter))
        send_to_influx((counter))
        sleep(3)
        print("Waiting for new impuls")
    else:
        print("---------------------Stoersignal-------------------------")

print("starting gas meter")
#Internet connection check
check_internet_on()
#GPIO connection setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
#Initialisation counter
counter = read_counter()

while True:
        check_internet_on()
        time_before_rising = wait_for_edge()
        check_if_impuls_high(GPIO.input(11), time_before_rising, counter)
        continue