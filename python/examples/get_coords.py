from pymycobot.mycobot import MyCobot
import time

mc = MyCobot('/dev/ttyTHS1', 1000000)
mc.power_on()
#print(mc.get_angles())

x = mc.get_servo_voltages()
print(f"voltages: {x}")

y = mc.get_servo_status()
print(f"status: {y}")

z = mc.get_servo_temps()
print(f"temps: {z}")

while True:
    coords = None
    angles = None

    mc.power_on()
    time.sleep(.5)

    mc.set_color(250, 0, 0)
    time.sleep(1)

    while coords is None:
        coords = mc.get_coords()
        time.sleep(.5)
    while angles is None:
        angles = mc.get_angles()
        time.sleep(.5)

    print(f"coords: {coords} angles: {angles}")
    
    mc.set_color(0, 250, 0)
    mc.power_off()
    time.sleep(1)
    
   
    time.sleep(2)
    


time.sleep(1)
mc.power_off() 