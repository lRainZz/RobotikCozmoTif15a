import cozmo
import time

from getObject import *
from getColor import *

from cozmo.util import distance_mm
from cozmo.util import speed_mmps

# use to determine color from detected cube
def lego_cube_color_space_detection(objectData):
    # camera resolution is 320x240

    # input corner values
    left_x  = objectData[1]
    left_y  = objectData[2]
    right_x = objectData[3]
    right_y = objectData[4]

    # calculating roughly 50% most inner pixels of the lego cube
    quarter_dist_x = ((right_x - left_x) / 4)
    quarter_dist_y = ((right_y - left_y) / 4)

    inner_left_x  = left_x  + quarter_dist_x
    inner_right_x = right_x - quarter_dist_x

    inner_left_y  = left_y  + quarter_dist_y
    inner_right_y = right_y - quarter_dist_y

    # convert percentages to rounded pixel values
    # -1 because values represent array indeces
    inlef_pix_y = round(inner_left_y  * 240) - 1
    inlef_pix_x = round(inner_left_x  * 320) - 1
    inrig_pix_y = round(inner_right_y * 240) - 1
    inrig_pix_x = round(inner_right_x * 320) - 1

    cutout_corners = [inlef_pix_x, inlef_pix_y, inrig_pix_x, inrig_pix_y]

    print(cutout_corners)

    return cutout_corners

def rotate_to_cube(coz, startData):
	left  = startData[1] # x value
	right = startData[3] # x value

	cube_mid = ((right - left) / 2) + left

	print("Cube mid: " + str(cube_mid))

	if cube_mid > 0.43 and cube_mid < 0.57:
		return True

	if cube_mid > 0.5:
		turn_degree = -5
	else:
		turn_degree = 5
	
	coz.turn_in_place(cozmo.util.Angle(degrees=turn_degree)).wait_for_completed()

	corrected_image      = coz.world.latest_image.raw_image
	corrected_objectData = getObject(corrected_image)

	rotate_to_cube(coz, corrected_objectData)


def drive_to_lego_cube(coz, startData):
	steps = 0
	color = -1
	
	while True:
		# locate the cube
		rotate_to_cube(coz, startData)

		# drive 5 cm before looking if close enough to cube	
		coz.drive_straight(distance_mm(30), speed_mmps(100)).wait_for_completed()

		currentImage = coz.world.latest_image.raw_image

		objectData = getObject(currentImage)

		# 5th value [4] represents Y value of lower right corner
		# if this value is above 80%, cozmo is near enough to the cube
		if objectData[4] >= 0.80:
			
			color_area      = lego_cube_color_space_detection(objectData)
			color           = getColorInRange(currentImage, color_area[0], color_area[1], color_area[2], color_area[3])

			break
		else:
			continue

	return color

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