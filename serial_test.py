import serial, time

s = serial.Serial('/dev/ttyUSB0', 115200)
print str(s)

while True:
    s.write(bytearray([255, 'l', 20]))
    s.write(bytearray([255, 'r', 20]))

    response = s.readline().decode("utf-8")
    print response
    time.sleep(0.02)
