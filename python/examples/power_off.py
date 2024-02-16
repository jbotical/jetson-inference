from pymycobot.mycobot import MyCobot
import time

main_angles = -58

mc = MyCobot('/dev/ttyTHS1',1000000)
mc.power_on()
time.sleep(1)
mc.set_color(0, 250, 0)
time.sleep(0.5)
mc.set_gripper_state(0, 100)
time.sleep(0.5)
mc.send_angles([0,(main_angles),(main_angles),25,0,45],35)
time.sleep(3)
mc.power_off()
time.sleep(1)

