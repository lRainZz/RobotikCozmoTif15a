#!/usr/bin/env python3

import cozmo
import time

from cozmo.objects import LightCube, LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import red_light,green_light,blue_light


def init_light_cubes(coz, cubes):
    print("Batteriestatus: "+str(coz.battery_voltage)+"V")
    coz.say_text("What a mess", use_cozmo_voice=False, in_parallel=True).wait_for_completed()

    cubes[0].set_lights(red_light)
    cubes[1].set_lights(green_light)
    cubes[2].set_lights(blue_light)

    while True:
        lookaround = coz.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = coz.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=45)
        lookaround.stop()

        if len(cubes) > 2:
            break
        else:
            coz.say_text("Couldn't find the light cubes. I'll try again.", use_cozmo_voice=False, in_parallel=True).wait_for_completed()

    return True