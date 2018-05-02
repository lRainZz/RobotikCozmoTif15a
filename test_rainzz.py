#!/usr/bin/env python3

import cozmo;
from interactWithLego import *;

def run_cozmo(cozmo: cozmo.robot.Robot):
    lock_lego_cube(cozmo, 50)

cozmo.run_program(run_cozmo)