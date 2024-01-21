import pygame as pg
import numpy as np
from Movement_operations import *

class Camera:
    def __init__(self, render, position):
        self.render = render
        self.position = np.array([*position,1]) #interesting operation
        self.forward = np.array([0,0,1,1])
        self.up = np.array([0, 1, 0, 1])
        self.right = np.array([1, 0, 0, 1])
        self.h_fov = np.pi/3
        self.v_fov = self.h_fov*(render.HEIGHT/render.WIDTH)
        self.near_plane = 0.1
        self.far_plane = 100
        self.moving_speed = 0.02
        self.rotation_speed = 0.01

        return

    def control(self):
        key = pg.key.get_pressed()
        # Linear movement (not normalized)
        if key[pg.K_a]:
            self.position -= self.right*self.moving_speed
        if key[pg.K_d]:
            self.position += self.right*self.moving_speed
        if key[pg.K_w]:
            self.position += self.forward*self.moving_speed
        if key[pg.K_s]:
            self.position -= self.forward*self.moving_speed
        if key[pg.K_q]:
            self.position += self.up*self.moving_speed
        if key[pg.K_e]:
            self.position -= self.up*self.moving_speed
        if key[pg.K_SPACE]:
            self.position = [0.001,0.001,0.001,1] # return to origin, make numbers close to 0 to avoid dumb
            # dive by 0 error in Object3d.screen_projection

        # Rotational movement
        ## I noticed that a full rotation about x changes the coords system from left handed to right handed
        if key[pg.K_LEFT]:
            self.camera_rotate(0,-self.rotation_speed)
        if key[pg.K_RIGHT]:
            self.camera_rotate(0,self.rotation_speed)
        if key[pg.K_UP]:
            self.camera_rotate(-self.rotation_speed,0)
        if key[pg.K_DOWN]:
            self.camera_rotate(self.rotation_speed,0)
        if key[pg.K_c]:
            self.forward = np.array([0, 0, 1, 1])
            self.up = np.array([0, 1, 0, 1])
            self.right = np.array([1, 0, 0, 1])

        return

    def camera_rotate(self,anglex,angley,anglez=0): # maybe we dont need z?
        rotate = rotatex_op(anglex) @ rotatey_op(angley) @ rotatez_op(anglez)
        self.forward = self.forward @ rotate
        self.right = self.right @ rotate
        self.up = self.up @ rotate
        return

    def translate_matrix(self):
        x,y,z,w = self.position
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [-x, -y, -z, 1]
        ])

    def rotate_matrix(self):
        rx, ry, rz, w = self.right
        fx, fy, fz, w = self.forward
        ux, uy, uz, w = self.up
        return np.array([
            [rx, ux, fx, 0],
            [ry, uy, fy, 0],
            [rz, uz, fz, 0],
            [0, 0, 0, 1]
        ])

    def camera_matrix(self):
        return np.dot(self.translate_matrix(),self.rotate_matrix()) # same thing as @, matrix multiplication

    def showtext(self, text, loc=(0,0)):
        self.render.screen.blit(text, loc)
