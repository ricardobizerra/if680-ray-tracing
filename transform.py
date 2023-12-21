import numpy as np
import math

def create_matrix(a1, a2, a3, a4):
    return np.array([a1, a2, a3, a4])

def affine_transform(vector, transform_type="", x=0, y=0, z=0, angle=0):
    if transform_type == 'translate':
        matrix = translate(x, y, z)
    elif transform_type == 'rotate_x':
        matrix = rotate_x(angle)
    elif transform_type == 'rotate_y':
        matrix = rotate_y(angle)
    elif transform_type == 'rotate_z':
        matrix = rotate_z(angle)
    else:
        print ("As transformações aceitas são 'translate', 'rotate_x', 'rotate_y', and 'rotate_z'.")

    vector_to_calc = np.append(vector, 1)
    result = np.dot(matrix, vector_to_calc)
    result_to_return = (result[0], result[1], result[2])
    print(f'{vector} => {result_to_return}')

    return result_to_return

# translation matrix
def translate(x, y, z):
    return create_matrix([1, 0, 0, x],
                         [0, 1, 0, y],
                         [0, 0, 1, z],
                         [0, 0, 0, 1])

# rotation matrix
def rotate_x(angle):
    return create_matrix([1, 0, 0, 0],
                         [0, math.cos(angle), -math.sin(angle), 0],
                         [0, math.sin(angle), math.cos(angle), 0],
                         [0, 0, 0, 1])

def rotate_y(angle):
    return create_matrix([math.cos(angle), 0, math.sin(angle), 0],
                         [0, 1, 0, 0],
                         [-math.sin(angle), 0, math.cos(angle), 0],
                         [0, 0, 0, 1])

def rotate_z(angle):
    return create_matrix([math.cos(angle), -math.sin(angle), 0, 0],
                         [math.sin(angle), math.cos(angle), 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1])
