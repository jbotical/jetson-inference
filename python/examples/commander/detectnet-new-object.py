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
from jetson_utils import videoSource, videoOutput, Log, cudaFont

from pymycobot.mycobot import MyCobot
import time
import gc

from config_service import ConfigService







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

speed1 = 45
slow_timer = 10

vert_0 = -180
vert_1 = 1
vert_2 = -44

class ArmState(Enum):
    Search = 0
    Grasp = 1
    Deliver = 2
    Target = 3
    Shutdown = 4

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

font = cudaFont()
def update_messages(state, last_command_message, targeting_info, font, img):
    font.OverlayText(img, 200, 100, f"{state.name}", 5, 5, font.White, font.Black)
    font.OverlayText(img, 200, 100, targeting_info, 5, 42, font.White, font.Black)
    font.OverlayText(img, 150, 75, last_command_message, 5, 78, font.White, font.Black)
    font.OverlayText(img, 150, 75, raw_outputs_message, 5, 105, font.White, font.Black)

    if not current_target_description is None:
        font.OverlayText(img, 150, 75, current_target_description, 5, 135, font.White, font.Black)


def shut_down(mc):

    main_angles = -58

    mc.set_color(0, 250, 0)
    time.sleep(0.5)
    mc.set_gripper_state(0, 100)
    time.sleep(0.5)
    mc.send_angles([0,(main_angles),(main_angles),25,0,45],35)
    time.sleep(3)
    mc.power_off()
    time.sleep(1)



mc = MyCobot('/dev/ttyTHS1', 1000000)
mc.power_on()
time.sleep(0.1)

config_service = ConfigService()

# Setup initial functionality
search_commands, j, \
    grasp_commands, k, \
    deliver_commands, l, \
    target_commands, m, \
    detection_filter = config_service.setup_actions(speed1, ArmState, movement, mc)

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

last_command_message = ""
targeting_info = ""
centered_count = 0
raw_outputs_message = ""
current_target_description = None
currnet_target_name = None
paused_count_seconds = 0
paused_count_seconds_max = 3
action_time_counter = 0
pick_up_override = False
target_override = False
out_of_bounds_counter = 0
deliver_angle_0_joey = 135
deliver_angle_0_kids = 125

while True:
    
    img = input.Capture()

    if img is None: # timeout
        continue  

    update_messages(state, last_command_message, targeting_info, font, img)

    # detect objects in the image (with overlay)
    detections = net.Detect(img, overlay=args.overlay)
    millis = int(round(time.time() * 1000))
    timeout_expired = millis > last_millis + slow_timer
    detected_class_id = None
    for detection in detections:
        print(detection)
        if state not in (ArmState.Grasp, ArmState.Deliver):
            print(f"item classID: {detection.ClassID} center: {detection.Center}")

        detected_class_id = detection.ClassID
        
        name = detection_filter.get(detected_class_id)
        motion_stopped = not mc.is_moving() and not mc.is_gripper_moving()
        if True and timeout_expired:
            if name is not None and state == ArmState.Search:
                take_image = False
                detected_coords = mc.get_coords()
                
                if not detected_coords is None:
                    print(f"--------> found a thing with id: {detected_class_id} named {name}!! ")
                    current_target_description = f"{name} - {detected_class_id} - ({detected_coords[0], detected_coords[1]})"
                    current_target_name = name
                    if name == "kids":
                        config_service.set_deliver_angle(150)
                    else:
                        config_service.set_deliver_angle(110)
                    deliver_commands = config_service.set_deliver_commands()
                    state = ArmState.Target

   

    # Process state changes
    if state == ArmState.Search:
        if not mc.is_moving() and not mc.is_gripper_moving() and timeout_expired:
            targeting_info = ""

            last_millis = millis

            command_name, params = search_commands[j]
            if command_name == "set_color":
                print(f"current state: {state.name}")
                mc.set_color(params[0], params[1], params[2])
            elif command_name == "send_angles":
                print(f"j = {j}")
                mc.send_angles(params[0], params[1])

            # index step counter
            if j < len(search_commands) - 1:
                j = j + 1
            else:
                j = 0

                #Reset state and report status
                gc.collect()
                get_status()


    elif state == ArmState.Target:
        
        if (not mc.is_moving() and not mc.is_gripper_moving() and timeout_expired) or target_override:
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
                    y_message = f"x: {int(x)} move right "
                    y_direction = 1
                    y_offset = 15
                #elif x > 875:
                elif x > 810:
                    y_message = f"x: {x} move left "
                    y_direction = -1
                    y_offset = -30
                else:
                    y_message = "y is centered "
                    y_direction = 0
                    y_offset = 0

                if y < 250:
                    x_direction = -1
                    x_message = f"y: {y} move down "
                    x_offset = 30
                elif y > 450:
                    x_message = f"y: {y} move up "
                    x_direction = 1
                    x_offset = -10
                else:
                    x_message = "x is centered "
                    x_direction = 0
                    x_offset = 0

                new_direction_message = f"{x_message} {y_message}"

                print(f"detected_Coors: {detected_coords}")
                new_coords = copy.deepcopy(coords)
                is_forced_search: bool = False

                # if it was found
                if not (detected_coords is None):
                    new_x = detected_coords[0] + x_offset
                    new_y = detected_coords[1] + y_offset
                    
                    move = False

                    if new_x > 100 and new_x < 210 \
                        and new_y > -240 and new_y < 250:
                            detected_coords[0] = new_x
                            detected_coords[1] = new_y
                            drift_offset = 2

                            move = True
                            last_command_message = "Moving.."
                    else:
                        #is_forced_search = True

                        # leveled coords to prevent drift
                        level_x = new_x
                        level_y = new_y
                        #level_z = detected_coords[2]
                        level_z = 200
                        level_coords = [ level_x, level_y, level_z, -180, 0, -45 ]
                        last_command_message = f"Out of operating bounds! level: {str(level_coords)} count: {out_of_bounds_counter}"

                        drift_offset = 2

                        #detected_coords = level_coords
                        #mc.send_coords(detected_coords, params[0], params[1])
                        #time.sleep(0.5)


                        # have it look over and see if it fixes the bounds issue
                        #detected_coords[3] = angle_3 + 1



                        move = True
                        out_of_bounds_counter += 1
                        if out_of_bounds_counter > 8:
                            state = ArmState.Grasp
                            centered_count = 0
                            action_time_counter = 0

                        #-180, 0 -45

                    # apply corrections
                    r_x = detected_coords[3] + drift_offset       # offset to account for drift
                    r_y = detected_coords[4] + drift_offset
                    detected_coords[3] = r_x
                    detected_coords[4] = r_y


                    targeting_info = f"new target: ({detected_coords[0]}, {detected_coords[1]}; {new_direction_message})"

                    raw_outputs_message = ""

                    for coord in detected_coords:
                        raw_outputs_message += f"{coord} | "

                    try:
                        if move:
                            mc.send_coords(detected_coords, params[0], params[1])
                    except Exception as e:
                        print(f"Error occured: {e}")
                    
                    if x_direction == 0 and y_direction == 0:
                        centered_count += 1

                        if centered_count > 2:
                            state = ArmState.Grasp
                            centered_count = 0
                            action_time_counter = 0
                    else:
                        center_count = 0

                    if is_forced_search:
                        state = ArmState.Search
                else:
                    last_command_message = "nothing was found, no move happened.."

            # index step counter
            if m < len(target_commands) - 1:
                m = m + 1
            else:
                m = 0
        else:
            action_time_counter += 1
            raw_outputs_message = f"TARGET action_time_counter: {action_time_counter}"
            if action_time_counter >= 51:
                state = ArmState.Search
                target_override = True
               

    elif state == ArmState.Grasp:
        if (not mc.is_moving() and not mc.is_gripper_moving() and timeout_expired) or pick_up_override:
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

                z_adder = 0
                x = new_coords[0]
                if x > 190:
                    z_adder = 5

                new_coords[2] = 110 + z_adder # z
                new_coords[3] = -180
                new_coords[4] = -4
                new_coords[5] = -48
                mc.send_coords(new_coords, params[0], params[1])
                del new_coords

            elif command_name == "pick_up":
                mc.send_coords(coords, params[0], params[1])
                pick_up_override = False

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
        else:
            action_time_counter += 1
            raw_outputs_message = f"GRASP action_time_counter: {action_time_counter}"
            if action_time_counter >= 40:
                pick_up_override = True

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
            if command_name == "reset":
                last_command_message = ""
                targeting_info = ""
                raw_outputs_message = ""
                current_target_description = None
                current_target_name = None
                action_time_counter = 0
                target_override = False
                out_of_bounds_counter = 0
                

            if l < len(deliver_commands) - 1:
                l = l + 1
            else:
                l = 0
                take_image = True
                state = ArmState.Search



    # render the image
    output.Render(img)

    # update the title bar
    output.SetStatus("{:s} | Network {:.0f} FPS | last: {:s}".format(args.network, net.GetNetworkFPS(), last_command_message))

    # print out performance info
    #net.PrintProfilerTimes()

    # exit on input/output EOS
    if not input.IsStreaming() or not output.IsStreaming():
        state = ArmState.Shutdown
        img = input.Capture()
        update_messages(state, last_command_message, targeting_info, font, img)
        time.sleep(0.5)
        # render the image
        output.Render(img)
        shut_down(mc)
        break
