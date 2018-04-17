#!/usr/bin/env python3

import cozmo;

def cozmo_program(coz: cozmo.robot.Robot):
	
	# look for all three cubes
	lookaround = coz.start_behavior(cozmo.behavior.BehaviorTypes.LookAroundInPlace)
	cubes = coz.world.wait_until_observe_num_objects(num=1, object_type=cozmo.objects.LightCube, timeout=60)
	lookaround.stop()
	
	if len(cubes) < 1:
		print('Coulnd''t locate cube.. aborting')
		
	elif len(cubes) == 1:
		print('found cube... proceeding')
	
		#drive to first cube
		cube = cubes[0]
		cube.set_lights(cozmo.lights.red_light)
		coz.say_text('Cube found').wait_for_completed()
		
		action = coz.dock_with_cube(cube, approach_angle=cozmo.util.degrees(0), num_retries=2)
		action.wait_for_completed()
		
		if action.has_succeeded:
			cube.set_lights(cozmo.lights.red_light)

cozmo.run_program(cozmo_program)