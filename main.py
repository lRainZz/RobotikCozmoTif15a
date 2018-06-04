import cozmo;

from initLightCubes import *;
from getObject import *;
from interactWithLego import *;
from getColor import *;

# use to detect color of cube infront of cozmo
def lego_cube_color_space():
    # camera resoltion is 320x240

    # leave 25% space at the edges for better result
    left_x  = 80
    left_y  = 60
    right_x = 240
    right_y = 180

    cutout_corners[0] = left_x
    cutout_corners[1] = left_y
    cutout_corners[2] = right_x
    cutout_corners[3] = right_y

    return cutout_corners

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
    inner_right_y = right_y + quarter_dist_y

    # [left_x, left_y, right_x, right_y]
    cutout_corners[0] = inner_left_x
    cutout_corners[1] = inner_left_y
    cutout_corners[2] = inner_right_x
    cutout_corners[3] = inner_right_y

    return cutout_corners
    

def sort_lego_cubes(cozRob: cozmo.robot.Robot):

    # start by searching and initializing the light cubes
    allFound = init_light_cubes(cozmo)

    # save current postion of cozmo
    # lift arm for free camera persp.
    startPos = cozmo.util.pose
    reset_lift_position(cozRob)

    # start searching for lego cubes and sort them
    foundLegoCubes = 0
    found_blue     = False
    found_red      = False
    fround_green   = False

    while True:
        curentImage = cozmo.robot.world.wait_for(cozmo.world.EvtNewCameraImage)
        objectData  = getObject(currentImage)

        # try to detect color so cozmo can decide if the cube is already sorted
        detected_color_area = lego_cube_color_space_detection(objectData)
        prob_color          = getColor(currentImage, detected_color_area[0], detected_color_area[1], detected_color_area[2], detected_color_area[3])

        # if the cube with the given color is already sorted
        # cozmo will turn further to search fo a new one
        if prob_color == 0 and found_red:
            cozRob.turn_in_place(cozmo.util.Angle(degrees=35))
            continue
        elif prob_color == 1 and found_green:
            cozRob.turn_in_place(cozmo.util.Angle(degrees=35))
            continue
        elif prob_color == 2 and found_blue:
            cozRob.turn_in_place(cozmo.util.Angle(degrees=35))
            continue

        if foundLegoCubes < 3:
            if objectData[0] >= 95:
                
                # rotate cozmo so he's facing the cube
                rotate_to_cube(cozmo, objectData)

                #drive cozmo to lego cube, 3 cm steps until he's about 5cm away
                drive_to_lego_cube(cozmo)

                # lock the lego cube under cozmo, using an approach of 10 cm
                # giving him 5 cm to set the cube straight
                lock_lego_cube(cozmo, 1000)
                
                # static color detection, image is made while cune is in front of cozmo
                get_color_image = cozmo.robot.world.wait_for(cozmo.world.EvtNewCameraImage)
                color_area = lego_cube_color_space()
                color = getColor(get_color_image, color_area[0], color_area[1], color_area[2], color_area[3])
                
                # decide which light cube is the correct one
                # save which cube color is sorted
                if color == 0:   # red   - drive to cube1
                    cube_pose = cube1.pose
                    found_red = True
                elif color == 1: # green - drive to cube 2
                    cube_pose    = cube2.pose
                    fround_green = True
                elif color == 2: # blue  - drive to cube 3
                    cube_pose  = cube3.pose
                    found_blue = True
                else:
                    # if color can not be determined, cozmo will return to his start point
                    # giving the opportunity to reset the cube
                    cozmo.robot.GoToPose(startPos)
                    continue

                # drive to correct light cube
                cozRob.go_to_pose(cube_pose).wait_for_completed()
                
                # reset lift and drive back 3 cm so cozmo can move freely
                reset_lift_position(cozRob)
                cozRob.drive_straight(distance_mm(-40), speed_mmps(100)).wait_for_completed()

                # drive back to the starting position so cozmo can sort the next cube
                cozmo.robot.go_to_pose(startPos).wait_for_completed()
                
                # count sorted cubes
                foundLegoCubes = foundLegoCubes + 1

                continue
            else:
                cozRob.turn_in_place(cozmo.util.Angle(degrees=35)) 
                continue
        else:
            break

    cozRob.say('I''m done', use_cozmo_voice=False, in_parallel=True)

cozmo.run_program(sort_lego_cubes, use_viewer=True)

