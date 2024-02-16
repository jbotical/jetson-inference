#!/usr/bin/env python3
#
# Copyright (c) 2020, NVIDIA CORPORATION. All rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
#



# OPENBLAS_CORETYPE=ARMV8 ./detectnet-object.py /dev/video0 

from enum import Enum
import sys
import argparse
import copy

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log

from pymycobot.mycobot import MyCobot
import time
import gc

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="box,labels,conf", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video sources and outputs
input = videoSource(args.input, argv=sys.argv)
output = videoOutput(args.output, argv=sys.argv)
	
# load the object detection network
net = detectNet(args.network, sys.argv, args.threshold)



# best
# movement_list.append([7.47, -4.21, -65.74, -10.63, -2.98, -37.26])
# movement_list.append([49.21, -4.3, -65.65, -10.19, -2.98, 7.11])
# movement_list.append([97.55, -12.12, -65.74, -8.61, -7.03, 55.45])
# movement_list.append([48.86, -43.5, -40.95, 5.18, -2.28, 2.98])
# movement_list.append([2.9, -46.58, -24.69, -12.74, 1.14, -45.43])
# movement_list.append([-25.92, -56.77, -12.04, -16.52, 0.35, -45.43])
# movement_list.append([-49.65, -30.67, -61.96, 6.67, 1.31, -94.57])
# movement_list.append([46.66, 29.61, -86.66, -27.33, -4.3, 3.51])

speed1 = 25
slow_timer = 150

vert_0 = -180
vert_1 = 1
vert_2 = -44

class ArmState(Enum):
    Search = 0
    Grasp = 1
    Deliver = 2
    Target = 3

def get_status():
    x = mc.get_servo_voltages()
    print(f"voltages: {x}")
    y = mc.get_servo_status()
    print(f"status: {y}")
    z = mc.get_servo_temps()
    print(f"temps: {z}")

def movement(commands: [], angles, speed=speed1):
    commands.append(("send_angles", (angles, speed)))
    return commands


mc = MyCobot('/dev/ttyTHS1', 1000000)
mc.power_on()
time.sleep(0.1)



search_commands = []
search_commands.append(("set_color", (0,0,250)))
# search_commands.append(("send_angles", ([7.47, -4.21, -65.74, -10.63, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([49.21, -4.3, -65.65, -10.19, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([97.55, -12.12, -65.74, -8.61, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([48.86, -43.5, -40.95, 5.18, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([2.9, -46.58, -24.69, -12.74, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([-25.92, -56.77, -12.04, -16.52, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([-49.65, -30.67, -61.96, 6.67, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([46.66, 29.61, -86.66, -27.33, vert_1, vert_2], speed1)))


# corrds
# movement(search_commands, [121.9, 7.8, 162.3, -176.27, vert_1, vert_2])
# movement(search_commands, [231.9, -37.1, 213.9, -170.88, vert_1, vert_2])
# movement(search_commands, [223.4, 106.0, 205.6, -168.79,vert_1, vert_2])
# movement(search_commands, [205.4, 183.6, 189.1, -167.6, vert_1, vert_2])
# movement(search_commands, [81.6, 222.0, 173.4, -173.15,vert_1, vert_2])
# movement(search_commands, [205.4, 183.6, 189.1, -167.6, vert_1, vert_2])
# movement(search_commands, [223.4, 106.0, 205.6, -168.79,vert_1, vert_2])
# movement(search_commands, [201.7, -158.7, 203.5, -176.12, vert_1, vert_2])
# movement(search_commands, [25.8, -260.5, 180.0, -176.08, -1.6, -44.97])
#search_commands.append(("send_angles", ([23.7, -102.1, 205.2, -174.73, -0.24, -49.71], speed1)))
#search_commands.append(("send_angles", ([90.2, -92.9, 229.1, -177.47, -2.63, -44.76], speed1)))
# movement(search_commands, [103.2, -148.3, 135.9, -179.15, -2.6, -46.77])
# movement(search_commands, [172.6, -51.0, 137.7, -176.42, -0.92, -43.13])
#search_commands.append(("send_angles", ([137.5, 41.1, 123.1, -178.21, 0.82, -45.06], speed1)))
# search_commands.append(("send_angles", ([75.1, -221.9, 226.2, -179.13, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([39.2, -121.5, 229.5, -176.59, vert_1, vert_2], speed1)))
# search_commands.append(("send_angles", ([131.6, -52.7, 224.6, -175.5, vert_1, vert_2], speed1)))


# angles
# movement(search_commands, [90.35, -40.07, -57.39, 7.55, -4.39, 45.96])
# movement(search_commands, [38.14, 45.7, -139.92, 6.85, -0.26, -6.59])
# #movement(search_commands, [35.85, 45.26, -144.14, 12.74, 2.98, -10.19])
# #movement(search_commands, [35.94, 45.26, -144.14, 12.39, -1.14, -9.05])
# # movement(search_commands, [35.94, 45.52, -144.58, 24.6, 12.91, 0.52])
# # movement(search_commands, [35.59, 45.7, -144.49, 10.28, -2.1, -8.34])
# #movement(search_commands, [35.85, 45.7, -144.31, 8.7, 0.17, -7.03])
# #movement(search_commands, [74.17, -3.25, -106.78, 23.99, -0.26, 31.72])
# movement(search_commands, [80.94, -52.29, -38.49, 6.41, 2.02, 38.84])
# movement(search_commands, [60.46, -56.77, -38.49, 14.41, -1.05, 15.64])
# movement(search_commands, [34.27, -57.12, -38.49, 9.75, -0.26, -9.49])
# movement(search_commands, [55.28, -8.26, -100.54, 20.56, -1.49, 14.85])
# movement(search_commands, [25.83, 6.67, -131.22, 36.12, -1.14, -14.76])
# movement(search_commands, [13.18, -52.47, -40.86, 6.85, -1.84, -31.81])
# movement(search_commands, [-16.52, -58.53, -40.34, 17.75, -1.4, -62.49])
# movement(search_commands, [-24.52, -21.18, -105.29, 42.8, -1.66, -66.09])
# # movement(search_commands, [-43.59, 4.83, -141.41, 51.5, -1.58, -79.8])
# # movement(search_commands, [-88.5, 4.74, -141.41, 49.65, 1.05, -135.52])
# # movement(search_commands, [-83.14, -35.33, -82.7, 31.9, 1.84, -129.46])
# movement(search_commands, [-41.22, -35.33, -82.7, 37.26, 0.26, -92.54])
# movement(search_commands, [-8.34, -34.98, -82.35, 34.1, -3.86, -58.0])
# movement(search_commands, [17.13, -34.98, -82.35, 31.64, -4.04, -29.53])

# good
# movement(search_commands, [51.59, 28.21, -93.77, -20.65, -0.7, 8.96])
# movement(search_commands, [78.48, -32.34, -35.06, -17.31, -3.07, 35.59])
# movement(search_commands, [47.46, -52.55, -10.28, -17.49, -0.96, 1.05])
# movement(search_commands, [5.53, -56.16, -10.54, -12.3, 2.1, -39.19])
# movement(search_commands, [-24.52, -60.64, -10.54, -11.42, 3.69, -68.9])
# movement(search_commands, [-50.8, -46.23, -10.63, -27.07, 2.63, -94.65])
# movement(search_commands, [-19.07, 17.05, -75.84, -25.57, 3.6, -63.36])

movement(search_commands, [73.82, 22.06, -91.23, -12.3, -3.07, 31.55])
movement(search_commands, [18.72, 10.45, -77.16, -15.55, 0.35, -30.41])
movement(search_commands, [-50.18, 11.16, -78.04, -20.12, 2.98, -96.24])
movement(search_commands, [-62.4, -34.54, -30.14, -21.88, 3.33, -106.43])
movement(search_commands, [-36.56, -34.98, -29.79, -21.18, 3.6, -81.29])
movement(search_commands, [7.64, -34.98, -30.23, -17.31, 2.02, -37.61])
movement(search_commands, [52.99, -35.06, -30.23, -17.05, 1.14, 8.26])
movement(search_commands, [89.82, -38.93, -29.97, -15.9, -6.85, 45.79])
movement(search_commands, [81.73, 16.69, -95.71, -7.2, -1.58, 37.0])
movement(search_commands, [27.24, 42.89, -122.34, -3.86, 0.43, -22.14])

j = 0


grasp_commands = []
grasp_commands.append(("set_color", (250,0,0)))
grasp_commands.append(("set_gripper_state", (0, 100)))
grasp_commands.append(("get_coords", None))
grasp_commands.append(("send_down", (30, 0)))
grasp_commands.append(("set_gripper_state", (1, 100)))
grasp_commands.append(("set_color", (0,250,0)))
grasp_commands.append(("pick_up", (30, 0)))
k = 0

delivery_speed = 40

deliver_commands = []
deliver_commands.append(("set_color", (150,150,0)))
deliver_commands.append(("send_angles", ([103.53, -15.55, -66.88, -2.72, -4.39, 59.32], delivery_speed)))
deliver_commands.append(("send_angles", ([131.74, -26.27, -59.15, -2.98, -1.84, 83.58], delivery_speed)))
deliver_commands.append(("set_gripper_state", (0, 100)))
deliver_commands.append(("send_angles", ([103.53, -15.55, -66.88, -2.72, -4.39, 59.32], delivery_speed)))
deliver_commands.append(("send_angles", ([60.38, -13.09, -57.56, -16.61, -2.37, 17.75], delivery_speed)))
l = 0

target_commands = []
target_commands.append(("set_color", (150,0,150)))
target_commands.append(("get_coords", (30, 0)))
target_commands.append(("do_move", (30, 0)))
m = 0



# start at the beginning
mc.send_angles([7.47, -4.21, -65.74, -10.63, -2.98, -37.26], speed1)
# only use a sleep outside of the main loop!
time.sleep(1)

last_millis = int(round(time.time() * 1000))

stopped_moving = False
coords = None

state = ArmState.Search
y_offset = 0

take_image = True

while True:
    if take_image:
        # capture the next image
        img = input.Capture()

    if img is None: # timeout
        continue  
        
    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)
    millis = int(round(time.time() * 1000))
    timeout_expired = millis > last_millis + slow_timer

    

    # Process state changes
    if state == ArmState.Search:
        if not mc.is_moving() and not mc.is_gripper_moving() and timeout_expired:
            last_millis = millis

            command_name, params = search_commands[j]
            if command_name == "set_color":
                print(f"current state: {state.name}")
                mc.set_color(params[0], params[1], params[2])
            elif command_name == "send_angles":
                print(f"j = {j}")
                mc.send_angles(params[0], params[1])
                #mc.send_coords(params[0], params[1])

            if j < len(search_commands) - 1:
                j = j + 1
            else:
                j = 0

                #Reset state and report status
                gc.collect()
                get_status()


    elif state == ArmState.Target:
        
        if not mc.is_moving() and not mc.is_gripper_moving() and timeout_expired:
            last_millis = millis
            
            x_direction = -1
            y_direction = -1
            command_name, params = target_commands[m]
            # commands
            if command_name == "get_coords":
                coords = mc.get_coords()

            elif command_name == "set_color":
                print(f"Current state: {state.name}")
                mc.set_color(params[0], params[1], params[2])

            elif command_name == "do_move":
                
                # targeting
                x, y = detection.Center


                if x < 575:
                    print("move right")
                    y_direction = 1
                    y_offset = 20
                elif x > 875:
                    print("move left")
                    y_direction = -1
                    y_offset = -60
                else:
                    print("y is centered")
                    y_direction = 0
                    y_offset = 0

                if y < 250:
                    x_direction = -1
                    print("move down")
                    x_offset = 50
                elif y > 450:
                    print("move up")
                    x_direction = 1
                    x_offset = -20
                else:
                    print("x is centered")
                    x_direction = 0
                    x_offset = 0

                print(f"do_move: x: {x} y: {y} x_direction: {x_direction} y_direction: {y_direction} coords: {coords}")
                print(f"detected_Coors: {detected_coords}")
                new_coords = copy.deepcopy(coords)

                # # Prevent going outside bounds
                # if coords[1] < -240 or coords[1] < detected_coords[1] - 100:
                #     print("reached lower Y bounds")
                #     state = ArmState.Search
                # elif coords[1] > 240 or coords[1] < detected_coords[1] + 100:
                #     print("reached upper Y bounds")
                #     state = ArmState.Search

                
                # # Determine new coordinates based on target data
                # if y_direction == 1: # move right
                #     new_coords[1] = coords[1] +  20 # y

                # elif y_direction == -1: # move left
                #     new_coords[1] = coords[1] - 20 # y

                # mc.send_coords(new_coords, params[0], params[1])
                ##del new_coords

                if not detected_coords is None:
                    detected_coords[0] = detected_coords[0] + x_offset
                    detected_coords[1] = detected_coords[1] + y_offset

                    mc.send_coords(detected_coords, params[0], params[1])
                    state = ArmState.Grasp

            # if x_direction == 0 and y_direction == 0 and detection is not None:
            #     print("locked on target, going to Grasp state")
            #     state = ArmState.Grasp


            if m < len(target_commands) - 1:
                m = m + 1
            else:
                m = 0
            

    elif state == ArmState.Grasp:
        if not mc.is_moving() and not mc.is_gripper_moving() and timeout_expired:
            last_millis = millis
            command_name, params = grasp_commands[k]
            
            # deteleme
            print(f"current state: {state.name}")

            # take_image = True
            # continue

            if command_name == "get_coords":
                coords = mc.get_coords()

            elif command_name == "send_down":
                new_coords = copy.deepcopy(coords)
                #new_coords = copy.deepcopy(detected_coords)
                new_coords[0] = new_coords[0] + 5
                new_coords[1] = new_coords[1] - 10 # y
                new_coords[2] = 110 # z
                new_coords[3] = -180
                new_coords[4] = -4
                new_coords[5] = -48
                mc.send_coords(new_coords, params[0], params[1])
                del new_coords

            elif command_name == "pick_up":
                mc.send_coords(coords, params[0], params[1])

            elif command_name == "set_gripper_state":
                mc.set_gripper_state(params[0], params[1])

            elif command_name == "set_color":
                print(f"current state: {state.name}")
                mc.set_color(params[0], params[1], params[2])

            elif command_name == "right_move":
                new_coords = copy.deepcopy(coords)
                new_coords[1] = coords[1] +  40 # y
                mc.send_coords(new_coords, params[0], params[1])
                del new_coords

            elif command_name == "left_move":
                new_coords = copy.deepcopy(coords)
                new_coords[1] = coords[1] - 40 # y
                mc.send_coords(new_coords, params[0], params[1])
                del new_coords

            if k < len(grasp_commands) - 1:
                k = k + 1
            else:
                k = 0
                state = ArmState.Deliver

    elif state == ArmState.Deliver:
        if not mc.is_moving() and not mc.is_gripper_moving() and timeout_expired:
            last_millis = millis
            command_name, params = deliver_commands[l]
            if command_name == "set_color":
                print(f"current state: {state.name}")
                mc.set_color(params[0], params[1], params[2])
            elif command_name == "send_angles":
                mc.send_angles(params[0], params[1])
            elif command_name == "set_gripper_state":
                mc.set_gripper_state(params[0], params[1])
            if command_name == "get_coords":
                coords = mc.get_coords()                

            if l < len(deliver_commands) - 1:
                l = l + 1
            else:
                l = 0
                take_image = True
                state = ArmState.Search


    detected_class_id = None
    for detection in detections:
        #print(detection)
        if state not in (ArmState.Grasp, ArmState.Deliver):
            print(f"item classID: {detection.ClassID} center: {detection.Center}")


        # toothbrush
        detected_class_id = detection.ClassID

        detection_filter = {}
        detection_filter[90] = "toothbrush"
        detection_filter[44] = "bottle"
        #detection_filter[82] = "thing 1"
        detection_filter[16] = "thing 2"
        detection_filter[35] = "thing 3"
        detection_filter[61] = "thing 4"
        detection_filter[49] = "thing 5"
        detection_filter[48] = "thing 6"
        detection_filter[43] = "thing 7"
        detection_filter[87] = "thing 8"

        
        name = detection_filter.get(detected_class_id)
        if name is not None and state == ArmState.Search:
            take_image = False
            detected_coords = mc.get_coords()
            print(f"--------> found a thing with id: {detected_class_id} named {name}!! ")
            
            state = ArmState.Target
            
            


    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    #net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        break
