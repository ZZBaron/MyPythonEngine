import pygame as pg
import numpy as np
from Object_3d import *
from Camera import *
from Projection import *
from Menu import *
from Mechanics import *

class SoftwareRender:
    def __init__(self):
        pg.init()
        self.FPS = 60
        self.RES = self.WIDTH, self.HEIGHT = 500, 500
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH//2, self.HEIGHT//2
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.create_objects()

        # debug
        self.cycle_num = 0
        return

    def create_objects(self):
        self.menu = Menu(self)
        self.camera = Camera(self, [0.5,0.5,-2])
        self.projection = Projection(self)
        self.camera_UI_font = pg.font.SysFont('times new roman', 30, bold=True)
        # self.rotatingcube = Object3d(self)
        # self.rotatingcube.translate([0,0,0])
        # self.rotatingcube.rotate(0,0,0)

        self.world_axes = Axes(self)
        self.world_axes.movement_flag = False

        # Create Objects
        self.particle1 = Particle(self, init_pos=[0,0,0], mass=1)
        self.particle1.movement_flag = True
        self.particle1.velocity = np.array([0,1,0])
        self.particle1.colors_v = [pg.Color('black')]

        self.particle2 = Particle(self, init_pos=[0,1,0], mass=1)
        self.particle2.movement_flag = True
        self.particle2.velocity = np.array([0,0,0])
        self.particle2.colors_v = [pg.Color('blue')]

        # Storing created objects
        self.current_particles = [self.particle1,self.particle2]


        # we should do self.particle = Particle(self, init_pos, pos_func,(or) movement_flag=False, mass, charge)


        self.cube = Cube(self)


        return

    def draw(self):
        self.screen.fill(pg.Color('black'))
        # self.rotatingcube.draw()
        self.world_axes.draw()
        # self.cube.draw()

        # vertices dont seem to draw when the cam is at same height

        self.particle1.draw()
        self.particle2.draw()

        time_since_launch = pg.time.get_ticks() / 1000
        text = self.camera_UI_font.render('t = ' + str(time_since_launch), True, pg.Color('white'))
        self.camera.showtext(text, loc=(0,1))

        current_pos = self.particle1.vertices[0][0:3]
        x,y,z = current_pos
        text = self.camera_UI_font.render('(x,y,z) = ' + '({:.4f},{:.4f},{:.4f})'.format(x,y,z), True, pg.Color('white'))
        self.camera.showtext(text, loc=(0, 30))

        # need to check for collisions
        for index, particle in enumerate(self.current_particles):
            l = len(self.current_particles)
            other_particles = self.current_particles[0:index] + self.current_particles[index+1:l]

            for other_particle in other_particles:
                # print(1,'   ',particle.velocity)
                # print(2,'   ',other_particle.velocity)
                x1,y1,z1 = particle.vertices[0][0:3]
                x2, y2, z2 = other_particle.vertices[0][0:3]
                # print(x1,y1,z1)
                if np.isclose(np.sqrt((x1-x2)**2+(y1-y2)**2+(z1-z2)**2),0, atol=0.01):
                    particle.velocity, other_particle.velocity = elastic_linear_collide(particle, other_particle)

        if self.menu.flag:
            self.menu.draw()


        return

    def run(self):
        looptime = 0
        while True:
            self.draw()
            self.camera.control()
            self.keys_pressed()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

            #debug
            self.cycle_num +=1

    def keys_pressed(self):
        key = pg.key.get_pressed()
        # Linear movement (not normalized)
        if key[pg.K_l]:
            self.particle1.movement_flag = not self.particle1.movement_flag #doesnt resume movement after unpausing
        if key[pg.K_ESCAPE]:
            self.menu.flag = not self.menu.flag

        return

# test = SoftwareRender()
# print(type(SoftwareRender))
# print(type(test))
if __name__ == '__main__':
    app = SoftwareRender()
    app.run()