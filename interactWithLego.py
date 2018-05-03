#!/usr/bin/env python3

import cozmo;
import time;
from cozmo.util import distance_mm;
from cozmo.util import speed_mmps;

def lock_lego_cube(cozmo, distance_in_mm):
	reset_lift_position(cozmo)

	cozmo.drive_straight(distance_mm(distance_in_mm), speed_mmps(100)).wait_for_completed()
	cozmo.drive_straight(distance_mm(-5), speed_mmps(100)).wait_for_completed()

	lift_to_lego_position(cozmo)

def lift_to_lego_position(coz):
	coz.move_lift(-2.2)
	time.sleep(0.33)
	coz.move_lift(0)

def reset_lift_position(coz, bottom=False):
	speed = 5

	if bottom:
		speed = -5
	
	coz.move_lift(speed)
	time.sleep(0.5)
	coz.move_lift(0)