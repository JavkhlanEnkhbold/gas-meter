from influxdb import InfluxDBClient
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

def wait_for_edge():
    GPIO.wait_for_edge(11, GPIO.RISING)
    time = datetime.now()
    print("Rising edge: ", time)
    sleep(2)
    return time

def read_counter():
    with open("counter.txt", "r") as file:
        lines = file.read().splitlines()
        last_line = lines[-1]
        return last_line

def write_counter_into_file(counter):
    with open("counter.txt","w") as file:
         file.write(str(counter))

def update_counter(counter):
    counter = int(counter)
    counter += 1
    write_counter_into_file(counter)
    return counter

def check_if_impuls_high(GPIO_PIN_Number, time_before_rise, counter):
    if GPIO_PIN_Number == GPIO.HIGH:
        print("HIGH")
        GPIO.wait_for_edge(11, GPIO.FALLING)
        time = datetime.now()
        print("Falling edge:", time)
        print("Impuls length: ", time-time_before_rise)
        sleep(1)
        new_counter = update_counter(counter)
        sleep(2)
        print("Impuls:", int(new_counter))
        send_to_influx(new_counter)
        sleep(3)
        print("Waiting for new impuls")
    else:
        print("---------------------Stoersignal-------------------------")

print("starting gas meter")
#GPIO connection setup
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

while True:
        counter = read_counter()
        time_before_rising = wait_for_edge()
        check_if_impuls_high(GPIO.input(11), time_before_rising, counter)
        continue