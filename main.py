import cozmo

from initLightCubes import *
from getObject import *
from interactWithLego import *
from getColor import *

# use to detect color of cube infront of cozmo
def lego_cube_color_space():
    # camera resoltion is 320x240

    # leave 25% space at the edges for better result
    left_x  = 80
    left_y  = 60
    right_x = 240
    right_y = 180

    cutout_corners = [left_x, left_y, right_x, right_y]

    return cutout_corners

def sort_lego_cubes(cozRob: cozmo.robot.Robot):

    cozRob.camera.color_image_enabled = True
    
    cube1 = cozRob.world.get_light_cube(LightCube1Id)
    cube2 = cozRob.world.get_light_cube(LightCube2Id)
    cube3 = cozRob.world.get_light_cube(LightCube3Id)

    cubes = [cube1, cube2, cube3]

    start_pos = cozRob.pose

    # start by searching and initializing the light cubes
    init_light_cubes(cozRob, cubes)

    # lift arm for free camera persp.
    reset_lift_position(cozRob)

    cozRob.go_to_pose(start_pos).wait_for_completed()

    cozRob.turn_in_place(cozmo.util.Angle(degrees=180)).wait_for_completed()

    # start searching for lego cubes and sort them
    foundLegoCubes = 0
    found_blue     = False
    found_red      = False
    found_green    = False

    first_false = True

    while True:        
        currentImage = cozRob.world.latest_image.raw_image
        objectData   = getObject(currentImage)

        if foundLegoCubes < 3:
            if objectData[0] >= 0.95:
                
                # try to detect color so cozmo can decide if the cube is already sorted
                detected_color_area = lego_cube_color_space_detection(objectData)
                prob_color          = getColorInRange(currentImage, detected_color_area[0], detected_color_area[1], detected_color_area[2], detected_color_area[3])

                # if the cube with the given color is already sorted
                # cozmo will turn further to search fo a new one
                if prob_color == 0 and found_red:
                    cozRob.turn_in_place(cozmo.util.Angle(degrees=35)).wait_for_completed()
                    continue
                elif prob_color == 1 and found_green:
                    cozRob.turn_in_place(cozmo.util.Angle(degrees=35)).wait_for_completed()
                    continue
                elif prob_color == 2 and found_blue:
                    cozRob.turn_in_place(cozmo.util.Angle(degrees=35)).wait_for_completed()
                    continue

                reset_head_position(cozRob, False, True)
                
                #drive cozmo to lego cube, 3 cm steps until he's about 5cm away
                color = int(drive_to_lego_cube(cozRob, objectData))

                print("color: " + str(color))

                # decide which light cube is the correct one
                # save which cube color is sorted
                if color == 0:   # red   - drive to cube1
                    cube_pose = cube1.pose
                    found_red = True
                elif color == 1: # green - drive to cube 2
                    cube_pose = cube2.pose
                    found_green = True
                elif color == 2: # blue  - drive to cube 3
                    cube_pose = cube3.pose
                    found_blue = True
                else:
                    # if color can not be determined, cozmo will return to his start point
                    # giving the opportunity to reset the cube
                    # reset_lift_position(cozRob)
                    # cozRob.go_to_pose(start_pos).wait_for_completed()
                    # continue
                    cube_pose = cube3.pose

                # lock the lego cube under cozmo, using an approach of 10 cm
                # giving him 5 cm to set the cube straight
                lock_lego_cube(cozRob, 150)

                # count sorted cubes
                foundLegoCubes = foundLegoCubes + 1

                # drive to correct light cube
                cozRob.go_to_pose(cube_pose).wait_for_completed()

                # reset lift and drive back 3 cm so cozmo can move freely
                reset_lift_position(cozRob)
                cozRob.drive_straight(distance_mm(-40), speed_mmps(100)).wait_for_completed()

                # return to start position
                cozRob.go_to_pose(start_pos).wait_for_completed()
                cozRob.turn_in_place(cozmo.util.Angle(degrees=180)).wait_for_completed()

                continue
            else:
                if first_false:
                    cozRob.turn_in_place(cozmo.util.Angle(degrees=-90)).wait_for_completed()
                    first_false = False

                cozRob.turn_in_place(cozmo.util.Angle(degrees=30)).wait_for_completed()
                continue
        else:
            break

    cozRob.say_text('I''m done', use_cozmo_voice=False, in_parallel=True)

cozmo.run_program(sort_lego_cubes, use_viewer=True)

