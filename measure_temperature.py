from datetime import datetime
import logging
import time
import sqlite3

from gpiozero import CPUTemperature
import RPi.GPIO as GPIO
import dht11

logging.basicConfig(level=logging.INFO)

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'


def make_table():
    """
    Only called once manually
    """
    conn = sqlite3.connect('room')
    c = conn.cursor()
    q = "CREATE TABLE room (date text, temperature real, humidity real, cpu_temperature real)"
    c.execute(q)
    conn.commit()
    return


def main():
    instance = dht11.DHT11(pin=4)
    cpu = CPUTemperature()
    retry_num = 0
    while True:
        result = instance.read()
        if result.is_valid():
            retry_num = 0

            # Create data
            now = datetime.now().strftime(DATE_FORMAT)
            tem = result.temperature
            hum = result.humidity
            cpu_tem = cpu.temperature
            data = (now, tem, hum, cpu_tem)

            # Insert into database
            q = 'INSERT INTO room VALUES (?,?,?,?)'
            with sqlite3.connect('room') as con:
                c = con.cursor()
                c.execute(q, data)
            logging.info(f'Inserted data: {data}')

        else:
            logging.warning(f'Error with code {result.error_code}')
            if retry_num <= 4:
                retry_num += 1
                logging.info(f'Retry: {retry_num}')
                time.sleep(1)
                continue
            else:
                logging.info('Give up retry')
        time.sleep(60)


if __name__ == '__main__':
    main()
