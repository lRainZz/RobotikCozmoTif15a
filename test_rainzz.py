import cozmo
import time

from interactWithLego import *

def run_cozmo(coz: cozmo.robot.Robot):

    reset_lift_position(coz)
    reset_head_position(coz, False, True)
    coz.drive_straight(distance_mm(-50), speed_mmps(100)).wait_for_completed()
    coz.drive_straight(distance_mm(80), speed_mmps(100)).wait_for_completed()

    while True:
        time.sleep(1)

cozmo.run_program(run_cozmo, use_viewer=True)