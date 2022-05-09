import time
import board
import displayio
import terminalio
from adafruit_display_text import label
import adafruit_displayio_sh1107
import adafruit_sht4x

i2c = board.I2C()
sht = adafruit_sht4x.SHT4x(i2c)
sht.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION

# SH1107 is vertically oriented 64x128
displayio.release_displays()
display_bus = displayio.I2CDisplay(i2c, device_address=0x3C)
WIDTH = 128
HEIGHT = 64
BORDER = 2

display = adafruit_displayio_sh1107.SH1107(display_bus, width=WIDTH, height=HEIGHT, rotation=0)
main_group = displayio.Group()
display.show(main_group)

temperature_label = label.Label(font=terminalio.FONT, text="", scale=1)
humidity_label = label.Label(font=terminalio.FONT, text=   "", scale=1)
day_label = label.Label(font=terminalio.FONT, text=   "T(24h): N/A", scale=1)
t_label = label.Label(font=terminalio.FONT, text=   "", scale=1)
plot_label = label.Label(font=terminalio.FONT, text=   "|"+ "-"*19 + "|", scale=1) ## [0,21]

for l,y in zip([temperature_label,humidity_label,plot_label,day_label,t_label],[5,15,27,40,50]):
    l.anchor_point = (0, 0)
    l.anchored_position = (0, y)
    main_group.append(l)

## Statistics
temperature, relative_humidity = sht.measurements
N = 60*24
last_day = [temperature for _ in range(N)]
Ex = 0.
Exx = 0.
minval = temperature
maxval = temperature
for i in range(N):
    Ex += last_day[i]
    Exx += last_day[i]**2.


tstart = time.time()
tcurr = tstart

while True:
    tcurr = time.time()
    tt = int(tcurr-tstart)
    if temperature < minval:
        minval = temperature
    if temperature > maxval:
        maxval = temperature

    temperature, relative_humidity = sht.measurements
    if tt % (60) == 0:
        lastval = last_day.pop()
        last_day.insert(0,temperature)
        Ex -= lastval
        Exx -= lastval**2.
        Ex += temperature
        Exx += temperature**2.
        day_label.text = "T(24h): %0.1f +-%0.1f C"%(Ex/float(N),(Exx/float(N)-(Ex/float(N))**2.)**.5)

    if maxval != minval:
        cval = int((temperature - minval)/(maxval-minval) * 19.0 + 0)
        if cval < 0: cval = 0
        if cval > 18: cval = 18
        plot_label.text = "|"+ "-"*(cval) + "*" + "-"*(18-cval)  + "|"
    temperature_label.text = "Temperature: %0.1f C"%(temperature)
    humidity_label.text    = "   Humidity: %0.1f %%"%(relative_humidity)
    t_label.text = "Up time: %2dd%2dh%2dm%2ds"%(tt//(60*60*24)%100,tt//(60*60)%24,tt//(60)%60,tt//1%60)


