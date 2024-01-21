import pygame as pg
import numpy as np
from Movement_operations import *

class Object3d:
    def __init__(self, render):
        self.render = render
        # v = (x,y,z,w) where w = 1
        # each x,y,z denote the postions of the vertices, last coord w=1 always for some reason
        self.vertices = np.array([(0,0,0,1),(0,1,0,1),(1,1,0,1),(1,0,0,1),
                                   (0,0,1,1),(0,1,1,1),(1,1,1,1),(1,0,1,1)])
        self.vertex_size = 6
        # only give 3 vertices if you want a triangle
        # really i think we should call this "self.face_forming_edges" to be more precise
        self.faces = np.array([(0,1,2,3),(4,5,6,7),(0,4,5,1),(2,3,7,6),
                               (1,2,6,5),(0,3,7,4)])
        self.velocity = np.array([0,0,0])


        shape = [self.vertices,self.faces]


        # I want to make a cylinder, can i do this by specifying a region in coord space and projecting
        # said region on the screen?
        self.font = pg.font.SysFont('comic sans', 30, bold=True)
        self.color_faces = [(pg.Color('orange'),face) for face in self.faces]
        self.color_vertices = [(pg.Color('red'), vertex) for vertex in self.vertices]
        self.colors_v = [pg.Color('red') for vertex in self.vertices]
        self.movement_flag, self.draw_vertices = True, True
        self.draw_faces = True
        self.label = ''

        return

    def translate(self,pos):
        self.vertices = self.vertices @ translate_op(pos) # @ is matrix multiplication, or np.dot(self.vertices,translate_op(pos))
        return

    def rotate(self,anglex,angley,anglez):
        self.vertices = self.vertices @ rotatex_op(anglex) @ rotatey_op(angley) @ rotatez_op(anglez)
        return

    def draw(self):
        self.screen_projection()
        if self.movement_flag:
            self.movement(self.pos_func)
        return



    def movement(self,pos_func): # only for particles for now
        t = pg.time.get_ticks()/1000
        x,y,z = pos_func(t)
        dt = self.render.clock.get_time()/1000

        #make sure self.velocity is np.array to multiply by dt
        # x,y,z = self.vertices[0][0:3] + self.velocity*dt

        self.vertices = np.array([(x,y,z,1)])
        # want to code in Lagrangian mechanics



        # need to calculate velocity

        # self.rotate(0,pg.time.get_ticks() % 0.005,0)
        return

    def screen_projection(self):
        vertices = np.dot(self.vertices,self.render.camera.camera_matrix())
        vertices = np.dot(vertices,self.render.projection.projection_matrix)
        vertices /= vertices[:,-1].reshape(-1,1) # divide the vertex vectors by w coord for normalization
        vertices[(vertices>1)|(vertices<-1)]=0 # dont draw vertices with components more than 1 or less than -1
        vertices = np.dot(vertices,self.render.projection.to_screen_matrix)
        vertices = vertices[:,:2] #2d slice
        color_vertices = [(color, vertex) for color, vertex in zip(self.colors_v,vertices)]


        if self.draw_faces:
            for index, color_face in enumerate(self.color_faces):
                color, face = color_face
                polygon = vertices[face]
                if not np.any((polygon==self.render.H_WIDTH)|(polygon==self.render.H_HEIGHT)):
                    pg.draw.polygon(self.render.screen, color,polygon,3)
                    if self.label:
                        text = self.font.render(self.label[index],True,pg.Color('white'))
                        self.render.screen.blit(text,polygon[-1])

        if self.draw_vertices:
            for index, color_vertex in enumerate(color_vertices):
                color, vertex = color_vertex
                if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)): # this np.any
                    # function causes a performance bottleneck, can optimize with "just in time" compiler numba
                    # print(vertex)
                    # print(color)
                    pg.draw.circle(self.render.screen, color, vertex, self.vertex_size)
        return

class Axes(Object3d):
    def __init__(self,render):
        super().__init__(render)
        self.vertices = np.array([(0,0,0,1),(1,0,0,1),(0,1,0,1),(0,0,1,1)])
        self.faces = np.array([(0,1),(0,2),(0,3)])
        self.colors = [pg.Color('red'), pg.Color('green'), pg.Color('blue')]
        self.color_faces = [(color,face) for color, face in zip(self.colors,self.faces)]
        self.draw_vertices = False
        self.label = 'XYZ'

        return

class Cube(Object3d):
    def __init__(self,render):
        super().__init__(render)
        self.vertices, self.faces = self.make_cube((0,0,0,1), 0.2)
        self.movement_flag = False
        self.vertex_size = 6
        return

    def make_cube(self,pivot, side_length):
        s = side_length
        p = pivot
        px, py, pz, w = p
        vertices = np.array([p, (px, py + s, pz, w), (px + s, py + s, pz, w), (px + s, py, pz, w),
                             (px, py, pz + s, w), (px, py + s, pz + s, w), (px + s, py + s, pz + s, w),
                             (px + s, py, pz + s, w)])
        faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6),
                          (1, 2, 6, 5), (0, 3, 7, 4)])
        return [vertices, faces]

class Particle(Object3d):
    def __init__(self,render, mass=0, charge=0,
                 init_vel=np.array([0,0,0]), init_pos = np.array([0,0,0])):
        super().__init__(render)
        self.mass = mass
        self.charge = charge
        x,y,z = init_pos
        self.vertices = np.array([(x, y, z, 1)])
        self.velocity = init_vel
        self.faces = np.array([])
        self.colors_v = [pg.Color('black')]
        self.vertex_size = 10
        self.draw_vertices = True
        self.draw_faces = False
        return

    def get_pos(self):
        x,y,z = self.vertices[0][0:3]
        return np.array([x,y,z])

    def get_vel(self):
        return self.velocity

    def set_pos(self, new_pos):
        x, y, z = new_pos
        self.vertices = np.array([(x,y,z,1)])
        return

    def pos_func(self, t):

        f = 3
        w = f*2*np.pi
        return (0,(np.sin(t)+1)/2,0)

# to do solid body dynamics, we can just find a parametrization
# of the surface with the origin being the center of mass, p(u,v) = (x,y,z), where (0,0,0) is
# the cm. translate by cm vector in R^3.












