#!/usr/bin/env python3

import cozmo;
import time;
from interactWithLego import *;

def run_cozmo(coz: cozmo.robot.Robot):
    coz.camera.color_image_enabled = True
    
    #lock_lego_cube(cozmo, 50)
    reset_lift_position(coz)
    reset_head_position(coz, True)


    while True:
        time.sleep(1)

def reset_head_position(coz, bottom=False):
    speed = 5

    if bottom:
        speed = -5

    coz.move_head(speed)
    time.sleep(0.5)
    coz.move_head(0)

cozmo.run_program(run_cozmo, use_viewer=True)