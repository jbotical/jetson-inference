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


# This assists in capturing images of things


# OPENBLAS_CORETYPE=ARMV8 ./detectnet-object.py /dev/video0 

from enum import Enum
import sys
import argparse
import copy

from jetson_inference import detectNet
from jetson_utils import videoSource, videoOutput, Log, saveImage

from pymycobot.mycobot import MyCobot
import time
import gc

from cv2 import *

# parse the command line
parser = argparse.ArgumentParser(description="Locate objects in a live camera stream using an object detection DNN.", 
                                 formatter_class=argparse.RawTextHelpFormatter, 
                                 epilog=detectNet.Usage() + videoSource.Usage() + videoOutput.Usage() + Log.Usage())

parser.add_argument("input", type=str, default="", nargs='?', help="URI of the input stream")
parser.add_argument("output", type=str, default="", nargs='?', help="URI of the output stream")
parser.add_argument("--network", type=str, default="ssd-mobilenet-v2", help="pre-trained model to load (see below for options)")
parser.add_argument("--overlay", type=str, default="none", help="detection overlay flags (e.g. --overlay=box,labels,conf)\nvalid combinations are:  'box', 'labels', 'conf', 'none'")
parser.add_argument("--threshold", type=float, default=0.5, help="minimum detection threshold to use") 

try:
	args = parser.parse_known_args()[0]
except:
	print("")
	parser.print_help()
	sys.exit(0)

# create video sources and outputs
input = None #videoSource(args.input, argv=sys.argv)
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

speed1 = 80
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
# take images from around it

search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
#movement(search_commands, [40.69, 55.72, -140.44, 5.0, 1.93, -3.33])
movement(search_commands, [18.54, 11.16, -42.27, -50.36, 5.71, -23.37])
 

search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [18.01, 10.81, -43.41, -51.15, 6.5, -22.06])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [17.92, 10.81, -43.06, -50.27, 2.63, -55.19])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [18.01, 10.81, -42.97, -55.01, -1.49, -113.46])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [18.01, 10.81, -42.97, -58.27, -4.39, -156.0])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [18.01, 10.81, -43.41, -59.15, -7.55, -174.11])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [18.28, 10.28, -43.06, -59.94, -6.85, -103.88])

search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [-45.7, -13.97, -128.4, 55.1, 24.69, 91.23])
#movement(search_commands, [-61.34, -11.77, -64.51, -40.86, 32.08, 179.64])

search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [-12.12, -34.36, -40.34, -36.73, 27.5, -62.66])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [10.81, -47.46, -38.58, -38.58, 12.74, -130.34])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [55.54, -49.13, -39.02, -51.06, -13.53, -135.35])
search_commands.append(("set_color", (255,0,0)))
search_commands.append(("save_pic",()))
search_commands.append(("set_color", (0,255,0)))
movement(search_commands, [42.36, -1.84, -68.81, -39.37, -7.55, -151.96])



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
        #img = input.Capture()
        img = None

    # if img is None: # timeout
    #     continue  
        
    # detect objects in the image (with overlay)
    #detections = net.Detect(img, overlay=args.overlay)
    #detections = net.Detect(img)
    detections = []
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
                print(f"j = {j} angles: {params[0]}")
                mc.send_angles(params[0], params[1])
                #mc.send_coords(params[0], params[1])
            elif command_name == "save_pic":
                print(f"Saving picture..")
                last_millis += 2000
                save_image = False
                if save_image:
                    image_path = f"/home/elephant/images/image_{int(time.time())}.jpg"
                    try:
                        #saveImage(image_path, img)
                        pass
                    except Exception as ex:
                        print(f"Error occured: {ex}")
                    print(f"Saved image to {image_path}")
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

        
        # name = detection_filter.get(detected_class_id)
        # if name is not None and state == ArmState.Search:
        #     take_image = False
        #     detected_coords = mc.get_coords()
        #     print(f"--------> found a thing with id: {detected_class_id} named {name}!! ")
            
        #     #state = ArmState.Target
            
            


    # render the image
    #output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS".format(args.network, net.GetNetworkFPS()))

    # print out performance info
    #net.PrintProfilerTimes()

    # exit on input/output EOS
    if not output.IsStreaming():
        break
