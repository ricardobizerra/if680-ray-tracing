import numpy as np

def create_matrix(a1, a2, a3, a4):
    return np.array([a1, a2, a3, a4])

def affine_transform(vector, a1, a2, a3, a4):
    matrix = create_matrix(a1, a2, a3, a4)
    vector_to_calc = np.append(vector, 1)

    result = np.dot(matrix, vector_to_calc)
    result_to_return = (result[0], result[1], result[2])
    print(f'{vector} => {result_to_return}')

    return result_to_return