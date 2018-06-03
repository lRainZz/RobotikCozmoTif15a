#!/usr/bin/env python3

import cozmo
import base64
import io
import time
import asyncio
import functools
import tkinter
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
            cozmo.world.EvtNewCameraImage, self.on_new_camera_image)

    def on_new_camera_image(self, evt, **kwargs):
        img = self.get_image()
        edges = cv2.Canny(img, 100, 200)
        # image bearbeiten cv2

    def get_image(self):
        raw = self.__robot.world.latest_image.raw_image
        png = cv2.imread(raw)
        return png

    async def run(self):

        while True:
            await asyncio.sleep(1)


async def cozmo_program(robot: cozmo.robot.Robot):
    camera = Camera(robot)
    await camera.run()

cozmo.robot.Robot.drive_off_charger_on_connect = False
cozmo.run_program(cozmo_program, use_viewer=True)
