#!/usr/bin/env python3

import cozmo
import base64
import io
import time
import asyncio
import functools
import cv2

from cozmo.lights import Color, Light


class Camera():
    def __init__(self,  robot: cozmo.robot.Robot):
        '''Constuctor'''
        # attributes
        self.__robot = robot
        self.__cube01 = None
        self.__latest_image = None

        # settings
        self.__robot.camera.image_stream_enabled = True
        self.__robot.camera.color_image_enabled = True

        # events
        self.__robot.add_event_handler(
            cozmo.objects.EvtObjectTapped, self.on_cube_tap)
        self.__robot.add_event_handler(
            cozmo.world.EvtNewCameraImage, self.on_new_camera_image)

    def do_photo(self):
        '''Get current image from cozmo camera'''
        print("Waiting for a picture...")

        # wait for a new camera image to ensure it is captured properly
        self.__robot.world.wait_for(cozmo.world.EvtNewCameraImage)
        print("Found a picture, capturing the picture.")

        # store the image
        self.__latest_image = self.__robot.world.latest_image.raw_image
        print("Captured picture. Saving picture.")

        if self.__latest_image is not None:
            self.__latest_image.save(time.strftime("%d%m%Y%H%M%S")+".jpg")
            cozmo.logger.info("Success")
        else:
            cozmo.logger.info("Error")
            return "Error: I have no photos"

    def cube_connected(self):
        '''Returns true if Cozmo connects to both cubes successfully.'''
        self.__cube01 = self.__robot.world.get_light_cube(
            cozmo.objects.LightCube2Id)
        print('cube')
        if self.__cube01 is not None:
            self.__cube01.set_lights(cozmo.lights.red_light)
        return not (self.__cube01 == None)

    def on_cube_tap(self, evt, obj, **kwargs):
        if obj.object_id == self.__cube01.object_id:
            self.do_photo()
####################################################################################################

    def on_new_camera_image(self, evt, **kwargs):
        image2 = self.get_image()
        cv2.rectangle(image2, (0, 0), (100, 100), (0, 255, 0), 3)

    def get_image(self):
        raw = self.__robot.world.latest_image.raw_image
        png = cv2.imread(raw)
        return image
####################################################################################################

    async def run(self):
        if not self.cube_connected():
            print('Cube did not connect successfully')
            return

        while True:
            await asyncio.sleep(1)


async def cozmo_program(robot: cozmo.robot.Robot):
    camera = Camera(robot)
    await camera.run()

cozmo.robot.Robot.drive_off_charger_on_connect = True
cozmo.run_program(cozmo_program, use_viewer=True, force_viewer_on_top=True)
