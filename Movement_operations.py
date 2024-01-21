import numpy as np

def translate_op(pos):
    tx, ty, tz = pos
    return np.array([
        [1,0,0,0],
        [0,1,0,0],
        [0,0,1,0],
        [tx,ty,tz,1]
    ])

def rotatex_op(a):
    return np.array(([
        [1, 0, 0, 0],
        [0, np.cos(a), np.sin(a), 0],
        [0, -np.sin(a), np.cos(a), 0],
        [0, 0, 0, 1]
    ]))

def rotatey_op(a):
    return np.array([
        [np.cos(a), 0, -np.sin(a), 0],
        [0, 1, 0, 0],
        [np.sin(a), 0, np.cos(a), 0],
        [0, 0, 0, 1]
    ])

def rotatez_op(a):
    return np.array([
        [np.cos(a), np.sin(a), 0, 0],
        [-np.sin(a), np.cos(a), 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def scale_op(factor):
    return np.array([
        [factor, 0, 0, 0],
        [0, factor, 0, 0],
        [0, 0, factor, 0],
        [0, 0, 0, 1]
    ])