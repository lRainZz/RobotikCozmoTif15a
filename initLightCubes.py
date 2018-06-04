#!/usr/bin/env python3

import cozmo
import time

from cozmo.objects import LightCube, LightCube1Id, LightCube2Id, LightCube3Id
from cozmo.lights import red_light,green_light,blue_light


def init_light_cubes(coz):
    print("Batteriestatus: "+str(coz.battery_voltage)+"V")
    coz.say_text("Hmm, hier sieht es aber schlimm aus!", use_cozmo_voice=False, in_parallel=True)

    cube1=coz.world.get_light_cube(LightCube1Id)
    cube1.set_lights(red_light)
    cube2=coz.world.get_light_cube(LightCube2Id)
    cube2.set_lights(green_light)
    cube3=coz.world.get_light_cube(LightCube3Id)
    cube3.set_lights(blue_light)

    while True:
        lookaround = coz.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
        cubes = coz.world.wait_until_observe_num_objects(num=3, object_type=cozmo.objects.LightCube, timeout=45)
        lookaround.stop()

        if len(cubes) > 2:
            break
        else:
            coz.say_text("Ich konnte nicht alle Cubes finden. Mal sehen ob ich sie jetzt besser sehe", use_cozmo_voice=False, in_parallel=True).wait_for_completed()

    return True