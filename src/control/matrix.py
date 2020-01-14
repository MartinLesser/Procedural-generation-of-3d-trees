import math

from model.constants import MIN_BRANCH_ROTATION


def mult(vector, float):
    """
    Multiplies a vector with a float and returns the result in a new vector.
    :param vector: List with elements of the vector.
    :param float: float is factor.
    :return: vector
    """
    new_vector = []
    for item in vector:
        new_vector.append(item * float)
    return new_vector

def multVectors(vector1, vector2):
    """
    Multiplies two vectors and returns the result as a new vector.
    :param vector1: List
    :param vector2: List
    :return: vector
    """
    new_vector = []
    for i in range(len(vector1)):
        new_vector.append(vector1[i] * vector2[i])
    return new_vector

def matrixMultVec(matrix, vector):
    """
    Multiplies a matrix with a vector and returns the result as a new vector.
    :param matrix: Matrix
    :param vector: vector
    :return: vector
    """
    new_vector = []
    x = 0
    for row in matrix:
        for index, number in enumerate(row):
            x += number * vector[index]
        new_vector.append(x)
        x = 0
    return new_vector

def add(vector1, vector2):
    """
    Adds a vector to a vector and returns the result as a new vector.
    :param vector1: vector
    :param vector2: vector
    :return: vector
    """
    new_vector = []
    for index, item in enumerate(vector1):
        new_vector.append(vector1[index] + vector2[index])
    return new_vector

def sub(vector1, vector2):
    """
    Subtracts a vector from a vector and returns the result as a new vector.
    :param vector1: vector
    :param vector2: vector
    :return: vector
    """
    new_vector = []
    for index, item in enumerate(vector1):
        new_vector.append(vector1[index] - vector2[index])
    return new_vector

def rotate_left_z(vector, angle):
    """
    Multiplies a vector with a matrix to rotate the vector.
    :param vector: vector
    :param angle: float dictates how many degrees the vector is rotated
    :return: vector
    """
    rotation_matrix =   [
            [   math.cos(math.radians(angle)),  -math.sin(math.radians(angle)), 0],
            [   math.sin(math.radians(angle)),   math.cos(math.radians(angle)), 0],
            [                               0,                               0, 1],
                        ]
    return matrixMultVec(rotation_matrix, vector)

def rotate_right_z(vector, angle):
    return rotate_left_z(vector, -angle)

def rotate_left_x(vector, angle):
    """
    Multiplies a vector with a matrix to rotate the vector.
    :param vector: vector
    :param angle: float dictates how many degrees the vector is rotated
    :return: vector
    """
    rotation_matrix = [
        [   1,                               0,                             0 ],
        [   0,   math.cos(math.radians(angle)), -math.sin(math.radians(angle))],
        [   0,   math.sin(math.radians(angle)), math.cos(math.radians(angle)) ],
                                            ]
    return matrixMultVec(rotation_matrix, vector)

def rotate_right_x(vector, angle):
    return rotate_left_x(vector, -angle)

def rotate_left_y(vector, angle):
    """
    Multiplies a vector with a matrix to rotate the vector.
    :param vector: vector
    :param angle: float dictates how many degrees the vector is rotated
    :return: vector
    """
    rotation_matrix =   [
            [   math.cos(math.radians(angle)),  0,  math.sin(math.radians(angle))],
            [   0,                              1,                              0],
            [   -math.sin(math.radians(angle)), 0,  math.cos(math.radians(angle))],
                        ]
    return matrixMultVec(rotation_matrix, vector)

def rotate_right_y(vector, angle):
    return rotate_left_y(vector, -angle)

def rotate_left_z_local(vector, point, angle):
    """
    Moves the vector to the coordinates origin, rotates it and moves it back. This is used for the rotation of the
    segments when generating the tree mesh.
    :param vector: vector is the new point which is calculated in a circle
    :param point: vector is the original point from the skeleton tree
    :param angle: float dictates how many degrees the vector is rotated
    :return: vector
    """
    rotation_z = [
            [   math.cos(math.radians(angle)),  -math.sin(math.radians(angle)), 0],
            [   math.sin(math.radians(angle)),   math.cos(math.radians(angle)), 0],
            [                               0,                               0, 1],
                                           ]
    v1 = matrixMultVec(rotation_z, sub(vector,point))
    v2 = add(v1, point)
    return v2

def rotate_left_y_local(vector, point, angle):
    """
    Moves the vector to the coordinates origin, rotates it and moves it back. This is used for the rotation of the
    segments when generating the tree mesh.
    :param vector: vector is the new point which is calculated in a circle
    :param point: vector is the original point from the skeleton tree
    :param angle: float dictates how many degrees the vector is rotated
    :return: vector
    """
    rotation_y = [
            [   math.cos(math.radians(angle)),  -math.sin(math.radians(angle)), 0],
            [   math.sin(math.radians(angle)),   math.cos(math.radians(angle)), 0],
            [                               0,                               0, 1],
                                           ]
    v1 = matrixMultVec(rotation_y, sub(vector,point))
    v2 = add(v1, point)
    return v2

def rotate_left_x_local(vector, point, angle):
    """
    Moves the vector to the coordinates origin, rotates it and moves it back. This is used for the rotation of the
    segments when generating the tree mesh.
    :param vector: vector is the new point which is calculated in a circle
    :param point: vector is the original point from the skeleton tree
    :param angle: float dictates how many degrees the vector is rotated
    :return: vector
    """
    rotation_x = [
            [   math.cos(math.radians(angle)),  0,  math.sin(math.radians(angle))],
            [   0,                              1,                              0],
            [   -math.sin(math.radians(angle)), 0,  math.cos(math.radians(angle))],
                                           ]
    v1 = matrixMultVec(rotation_x, sub(vector,point))
    v2 = add(v1, point)
    return v2
