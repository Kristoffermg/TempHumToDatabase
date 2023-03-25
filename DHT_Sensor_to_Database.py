import Adafruit_DHT
import mysql.connector
from datetime import datetime
import time

database = mysql.connector.connect(
    host = 'kristofferhusdata.mysql.database.azure.com',
    user = 'kris',
    passwd = '',
    database = 'kristofferhusdata'
)

cursor = database.cursor()

print("Success connecting to database")

DHT_SENSOR = Adafruit_DHT.DHT22
DHT_PIN = 4

print("Delay until second is 0 starting...")
dt = datetime.now()
time.sleep(60 - dt.second)

while True:
    humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)
    dateValue = datetime.today().strftime('%Y-%m-%d %H:%M')
    dt = datetime.now()
    
    if humidity is not None and temperature is not None:
        print(dt.minute)
        if dt.minute == 0 or dt.minute == 30:
            cursor.execute(f"insert into ClimateInformation values('{dateValue}', {int(temperature)}, {int(humidity)})")
            database.commit()
            print(f"Inserted values {dateValue}, {temperature}, {humidity} into database")
    else:
        print("Failed to retrieve data from humidity sensor")
    time.sleep(60)
    