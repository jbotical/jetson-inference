class ConfigService():
    def __init__(self):
        pass


    def setup_actions(self, speed1, ArmState, movement, mc):
        search_commands = []
        search_commands.append(("set_color", (0,0,250)))

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
        deliver_commands.append(("reset", ()))
        deliver_commands.append(("send_angles", ([103.53, -15.55, -66.88, -2.72, -4.39, 59.32], delivery_speed)))
        deliver_commands.append(("send_angles", ([60.38, -13.09, -57.56, -16.61, -2.37, 17.75], delivery_speed)))
        deliver_commands.append(("send_angles", ([2.9, -6.41, -45.79, -30.58, 6.67, -42.18], delivery_speed)))

        l = 0

        target_commands = []
        target_commands.append(("set_color", (150,0,150)))
        target_commands.append(("get_coords", (30, 0)))
        target_commands.append(("do_move", (30, 0)))
        m = 0

        detection_filter = {}
        detection_filter[90] = "toothbrush"
        detection_filter[44] = "bottle"

        detection_filter[16] = "thing 2"
        detection_filter[35] = "thing 3"
        detection_filter[61] = "thing 4"
        detection_filter[49] = "thing 5"
        detection_filter[48] = "thing 6"
        detection_filter[43] = "thing 7"
        detection_filter[87] = "thing 8"

        # custom dataset
        detection_filter[1] = "joey"
        detection_filter[2] = "kids"



        return search_commands,j,grasp_commands,k,deliver_commands,l,target_commands,m,detection_filter



