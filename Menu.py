import pygame as pg
import numpy as np


class Menu:
    def __init__(self, render):
        self.render = render
        self.state = 'main'
        self.flag = False
        self.faces = np.array([(0,2,3,1)])
        self.color_faces = [(pg.Color('black'),face) for face in self.faces]
        # these are vertices that will be on the screen, in 2d
        self.vertices = [(1,1), (1,150), (150,1), (150,150)]
        return

    # works terribly
    def draw(self):
        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            print(face)
            polygon = [self.vertices[i] for i in self.faces[index]]
            print(polygon)
            if not np.any((polygon == self.render.H_WIDTH) | (polygon == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, color, polygon, 3)
                # if self.label:
                #     text = self.font.render(self.label[index], True, pg.Color('white'))
                #     self.render.screen.blit(text, polygon[-1])

        return