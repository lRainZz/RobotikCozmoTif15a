#!/usr/bin/env python3

import cozmo;
import time;

from cozmo.util import distance_mm;
from cozmo.util import speed_mmps;


def rotate_to_cube(cozmo, objectData):
	left  = objectData[1] # x value
	right = objectData[3] # x value

	# cozmo field of view ~ 60°
	# calculate turn percentage by substracting the mid (0,5) from the mid of the lego cube
	# calculate turn deg, by taking the cozmo fov of 60 and multiply it with the turn percentage
	cube_mid  = right - left
	turn_deg  = (cube_mid - 0,5) * 60	
	
	# turn cozmo to cube
	cozmo.turn_in_place(cozmo.util.Angle(degrees=turn_deg)) 


def drive_to_lego_cube(cozmo):
	while True:
		# drive 3 cm before looking if close enough to cube	
		cozmo.drive_straight(distance_mm(30), speed_mmps(100)).wait_for_completed()

		reset_head_position(cozmo, False, True)
		curentImage = cozmo.robot.world.wait_for(cozmo.world.EvtNewCameraImage)

		objectData = getObject(currentImage)

		# 5th value [4] represents Y value of lower right corner
		# if this value is above 95%, cozmo is near enough to the cube
		if objectData[4] >= 95:
			break
		else:
			continue

	return true

def lock_lego_cube(cozmo, distance_in_mm):
	reset_lift_position(cozmo)

	cozmo.drive_straight(distance_mm(distance_in_mm), speed_mmps(100)).wait_for_completed()

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

def reset_head_position(coz, bottom=False, middle=False):
	speed = 5

	if bottom:
		speed = -5

	if middle:
		coz.move_head(5)
		time.sleep(0.5)
		coz.move_head(-1)
		time.sleep(1)
		coz.move_head(0)
	else:
		coz.move_head(speed)
		time.sleep(0.5)
		coz.move_head(0)