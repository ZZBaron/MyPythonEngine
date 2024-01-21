import pygame as pg
import numpy as np

# input
# Partcle collsion:
def elastic_linear_collide(particle1,particle2):
    v1 = particle1.velocity
    v2 = particle2.velocity
    m1 = particle1.mass
    m2 = particle2.mass
    # conservation of momentum, and energy leads to
    vel1 = (m1*v1 - m2*v1 + 2*m2*v2)/(m1+m2)
    vel2 = (m2*v2 - m1*v2 + 2*m1*v1)/(m1+m2)
    return vel1, vel2


def lagrangian(tot_kinetic,tot_potential):
    return tot_kinetic - tot_potential
