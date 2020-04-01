from numpy import arange
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x=0, y=0, weight=1):
        self.x = x
        self.y = y
        self.weight = weight

    def __str__(self):
        return f"|{self.x:10.2f} | {self.y:10.2f} | {self.weight:10.2f} |"


def print_matrix(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            print(f"{matrix[i][j]:15.2f}", end = '')
        print("\n")


def print_table(table):
    print(" ------------------------------------- ")
    print("|     X     |     Y      |   weight   |")
    print(" ------------------------------------- ")
    for i in range(len(table)):
        print(table[i])
    print(" ------------------------------------- ")


def read_from_file(filename):
    points = list()
    with open(filename, "r") as f:
        line = f.readline()
        while line:
            x, y, weight = map(float, line.split())
            points.append(Point(x, y, weight))
            line = f.readline()
    return points


def append_right_side(matrix, points):
    for i in range(len(matrix)):
        res = 0
        for j in range(len(points)):
            res += points[j].weight * points[j].y * points[j].x ** i
        matrix[i].append(res)


def get_coeff(points, degree):
    coeff = 0
    for i in range(len(points)):
        coeff += points[i].weight * points[i].x ** degree
    return coeff


def find_slae_matrix(points, degree):
    matrix = [[get_coeff(points, j + i) for i in range(degree + 1)] for j in range(degree + 1)]
    append_right_side(matrix, points)
    return matrix


def get_polynomial_coeffs(matrix):
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i == j:
                continue
            mult = matrix[j][i] / matrix[i][i]
            for k in range(0, len(matrix) + 1):
                matrix[j][k] -= mult * matrix[i][k]

    for i in range(len(matrix)):
        mult = matrix[i][i]
        for j in range(len(matrix[i])):
            matrix[i][j] /= mult

    return [matrix[i][-1] for i in range(len(matrix))]


def add_plot(coeffs, label, start, end):
    my_x = list()
    my_y = list()
    step = (end - start) / 1000
    for x in arange(start, end + step, step):
        my_x.append(x)
        y = 0
        for i in range(len(coeffs)):
            y += coeffs[i] * x ** i
        my_y.append(y)

    plt.plot(my_x, my_y, label=label)



def add_table(table, label):
    table_x = [table[i].x for i in range(len(table))]
    table_y = [table[i].y for i in range(len(table))]

    plt.plot(table_x, table_y, 'o', label=label)


def draw_result():
    plt.legend()

    plt.xlabel('Размеры') 
    plt.ylabel('Время')

    plt.grid()
    plt.show()



if __name__ == "__main__":
    filename = "input.txt" # input("Enter filename: ")
    points = read_from_file(filename)

    if not points:
        print("Error occured while reading data from the file!")
        exit(1)

    print_table(points)

    try:
        degree = int(input("Enter polynomial degree: "))
    except:
        print("Error occured while reading int!")
        exit(1)
    if degree > len(points) - 1:
        print("Polynomial degree is too big. Error!")
        exit(1)

    slae_matrix = find_slae_matrix(points, degree)
    # print("\n\nMATRIX TO SOLVE:\n")
    # print_matrix(slae_matrix)
    # print("\nSOLVED MATRIX:\n")
    coeffs = get_polynomial_coeffs(slae_matrix)
    # print_matrix(slae_matrix)

    add_table(points, "table")
    add_plot(coeffs, "polynomial", points[0].x, points[-1].x)

    draw_result()
