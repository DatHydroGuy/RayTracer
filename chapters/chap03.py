from matrices import Matrix
from tuples import Tuple


def run():
    # Inverse of the identity = the identity
    matrix = Matrix.identity(4).inverse()
    for row in matrix.matrix:
        print(row)

    print()

    # Matrix * it's inverse = the identity
    matrix = Matrix([[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]])
    inv = matrix.inverse()
    mult = matrix * inv
    for row in mult.matrix:
        print(row)

    print()

    # Inverse of transpose = transpose of the inverse
    matrix = Matrix([[3, -9, 7, 3], [3, -8, 2, -9], [-4, 4, 4, 1], [-6, 5, -1, 1]])
    trans = matrix.transpose()
    inv_trans = trans.inverse()
    inv = matrix.inverse()
    trans_inv = inv.transpose()
    for i in range(4):
        print(f'{inv_trans.matrix[i]}\t\t\t{trans_inv.matrix[i]}')

    print()

    # Identity * tuple = tuple
    a = Matrix.identity(4)
    b = Tuple(1, 2, 3, 4)
    mult = a * b
    for elem in mult.vec:
        print(elem)

    print()

    # Modified identity * tuple
    a = Matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 4, 0], [0, 0, 0, 1]])
    b = Tuple(1, 2, 3, 4)
    mult = a * b
    for elem in mult.vec:
        print(elem)

    print()

    # Modified identity * tuple
    a = Matrix([[1, 0, 0, 0], [0, 1, 0, 3], [0, 0, 1, 0], [0, 0, 0, 1]])
    b = Tuple(1, 2, 3, 4)
    mult = a * b
    for elem in mult.vec:
        print(elem)


if __name__ == '__main__':
    run()
