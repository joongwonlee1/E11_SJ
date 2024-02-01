import adafruit_bme680
import time
import board
import pandas as pd

i2c= board.I2C()
bme680 = adafruit_bme680.Adafruit_BME680_I2C(i2c)

bme680.sea_level_pressure = 1013.25
#start = time.time()
lst = []

for i in range(10):
	sublst = []
	sublst.append(time.time())
	sublst.append("%0.1f" % bme680.temperature)
	sublst.append("%d" % bme680.gas)
	sublst.append("%0.1f" % bme680.relative_humidity)
	sublst.append("%0.3f" % bme680.pressure)
	sublst.append("%0.2f" %bme680.altitude)
	lst.append(sublst)
	time.sleep(1)


col_names = ["Time","Temperature", "Gas","Humidity", "Pressure", "Altitude"]
df = pd.DataFrame(lst, columns = col_names)
csv_data = df.to_csv('weather_data.csv', index = False)
