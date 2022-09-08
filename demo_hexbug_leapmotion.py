import pdb
import time
import Leap
import numpy as np
from time import sleep
from psychopy import visual
import serial.tools.list_ports
from getkey import getkey, keys

PSYCHOPY_PLOT = True

class LeapMotion:
    # https://developer-archive.leapmotion.com/documentation/python/devguide/Leap_Pointables.html
    # https://developer-archive.leapmotion.com/documentation/csharp/api/Leap.Finger.html
    def __init__(self):
        self.controller = Leap.Controller()
        self.fingers = {'thumb': 0,
                        'index': 1,
                        'middle': 2,
                        'ring': 3,
                        'pinky': 4}

        while not self.controller.is_connected:
            sleep(.5)

    def get_time_visible(self, finger_index=0):
        frame = self.controller.frame()
        time_visible = frame.fingers[finger_index].time_visible#.__getitem__(index=0)
        time_visible = np.round(time_visible, 2)
        return time_visible

    def get_tip_velocity(self, frame, finger_index=0, axis_index=0):
        velocity = frame.fingers[finger_index].tip_velocity.__getitem__(index=axis_index)
        return velocity

    def calc_dist(self, finger_from: str, finger_to: str):
        frame = self.controller.frame()
        pos_from = frame.fingers[self.fingers[finger_from]].tip_position
        pos_to = frame.fingers[self.fingers[finger_to]].tip_position
        return pos_from.distance_to(pos_to)

    def calc_speed(self):
        frame = self.controller.frame()
        velocities_x = [self.get_tip_velocity(frame, finger_index=i, axis_index=0) for i in range(5)]
        velocities_y = [self.get_tip_velocity(frame, finger_index=i, axis_index=1) for i in range(5)]
        velocities_z = [self.get_tip_velocity(frame, finger_index=i, axis_index=2) for i in range(5)]
        v_x = np.mean(velocities_x)
        v_y = np.mean(velocities_y)
        v_z = np.mean(velocities_z)
        v_x = np.round(v_x, 2)
        v_y = np.round(v_y, 2)
        v_z = np.round(v_z, 2)
        return v_x, v_y, v_z

######################################################
# PySerial

print('Scanning serial ports...\n')
ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

N_ports = len(ports)
portsList = list()

cnt = 0
for onePort in ports:
    portsList.append(str(onePort))
    print("Port number #{} \t| Device: {}".format(cnt, onePort.device))
    cnt += 1

port_number = -1
port_get_input = False # use port 1, when not asking for input
while (port_number==-1):
    if port_get_input:
        port_number_str = input("\nSelect Port number (from {} to {}): ".format(0, N_ports-1))
    else:
        port_number_str = 1
    try:
        port_number = int(port_number_str)
        if (port_number<0):
            print('Port number {} was invalid (negative). Retry...'.format(port_number))
        elif (port_number>=N_ports):
            print('Port number {} was invalid. Only {} port(s) exist(s).'.format(port_number, N_ports))
            port_number = -1
    except:
        print('Port number was invalid. Retry...')

portVar = ports[port_number].device
serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()
print('\nPySerial instance is running...\n')

######################################################
# LeapMotion and PsychoPy window

leapmotion = LeapMotion()
print('\nLeapMotion controller is running...\n')

if PSYCHOPY_PLOT:
    window = visual.Window(
        colorSpace='rgb',
        color=0.3,
        fullscr=False,
        size=(600, 600),
        allowGUI=True,
        units='pix')

    # x-axis (left/right) : blue color
    circle_x = visual.Circle(window, size=1, autoDraw=True,
                           lineColor=[-1, -1, 1],
                           lineWidth=5,
                            )
    # y-axis (up/down) : green color
    circle_y = visual.Circle(window, size=1, autoDraw=True,
                             lineColor=[-1, 1, -1],
                             lineWidth=5,
                            )
    # z-axis (forward/backward) : red color
    circle_z = visual.Circle(window, size=1, autoDraw=True,
                             lineColor=[1, -1, -1],
                             lineWidth=5,
                             )
    print('\nPsychoPy window is running...\n')
######################################################

MIN_VAL = 30.0
MAX_VAL = 130.0
ANALOG_MAX = 255
sleep_time_move = 0.8
time_hand_visible = 2.0
sleep_time_default = 0.02
certainty_thres = 100
vx_thres = 170
vy_thres = 170

last_cmd_time = time.time()

while True:
    time_since_last_cmd = time.time() - last_cmd_time
    time_visible = leapmotion.get_time_visible(finger_index=0)
    vx, vy, vz = leapmotion.calc_speed()
    if PSYCHOPY_PLOT:
        circle_x.size = np.abs(vx)
        circle_y.size = np.abs(vy)
        circle_z.size = np.abs(vz)
        text_stim_time_vis = visual.TextStim(window,
                                        'Time_hand instance is visible: {:.2f}'.format(time_visible),
                                        color=(1, 1, 1),
                                        pos=(0, 250),
                                        colorSpace='rgb'
                                         )
        if time_visible > time_hand_visible:
            text_stim_time_vis.color = (-1, -1, -1)
        text_stim_time_vis.draw()
        text_stim_time_cmd = visual.TextStim(window,
                                         'Time since last command: {:.2f}'.format(time_since_last_cmd),
                                         color=(1, -1, -1),
                                         pos=(0, 220),
                                         colorSpace='rgb'
                                         )
        if (time_visible > time_hand_visible) and (time_since_last_cmd > sleep_time_move):
            text_stim_time_cmd.bold = True
            text_stim_time_cmd.color = (-1, 1, -1),
        text_stim_time_cmd.draw()
        window.flip()
    if time_visible>time_hand_visible:
        do_move = False
        vx_abs = np.abs(vx)
        vy_abs = np.abs(vy)
        vz_abs = np.abs(vz)
        if (vx_abs-vy_abs)>certainty_thres:
            # left/right
            if vx>vx_thres:
                # right
                key_ = 'd'
                do_move = True
            elif vx<-vx_thres:
                # left
                key_ = 'a'
                do_move = True
            else:
                pass
        elif (vy_abs-vx_abs)>certainty_thres:
            # forward/backward
            if vy > vy_thres:
                # forward
                key_ = 'w'
                do_move = True
            elif vy < -vy_thres:
                # backward
                key_ = 's'
                do_move = True
            else:
                pass
        else:
            pass
        if do_move:
            if (time.time() - last_cmd_time)>sleep_time_move:
                serialInst.write(key_.encode('utf-8'))
                last_cmd_time = time.time()
        sleep(sleep_time_default)
