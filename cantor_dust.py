from matplotlib import pyplot as plt
from scipy.misc import imresize
import numpy as np
import math
import os

num_its = 5


def mutate(array):
    new_array = np.zeros(np.array(array.shape) * 3)

    cell_types = {
        0: np.zeros((3, 3)),
        1: np.array(
            [
                [1, 0, 1],
                [0, 0, 0],
                [1, 0, 1]
            ]
        )
    }

    for row in range(array.shape[0]):
        for col in range(array.shape[1]):
            new_array[
                    row * 3: (row + 1) * 3, col * 3: (col + 1) * 3
                ] = cell_types[array[row, col]]

    return new_array


def main():
    data_dir = './data'
    data_filepath = os.path.join(data_dir, 'coords_1.txt')
    with open(data_filepath) as fd:
        coord_strings = fd.read().splitlines()

    data_numpy = [
        np.array([
            np.array(list(map(int, byte)))
            for byte in coord_string.split()
        ]).transpose()
        for coord_string in coord_strings
    ]

    out_dir = './output'
    if not os.path.isdir(out_dir):
        os.makedirs(out_dir)

    for line_number, line in enumerate(data_numpy):
        this_out_dir = os.path.join(out_dir, str(line_number))
        if not os.path.isdir(this_out_dir):
            os.makedirs(this_out_dir)
            os.makedirs(os.path.join(this_out_dir, 'inverse'))
            os.makedirs(os.path.join(this_out_dir, 'standard'))

        for inversed in ['inverse', 'standard']:
            if inversed == 'inverse':
                res = np.logical_not(line)
            else:
                res = line

            resize_fac = 5000
            for i in range(num_its):
                print(res.nbytes / (1024 * 1024))
                to_save = imresize(
                    res,
                    math.ceil(resize_fac),
                    interp='nearest'
                )
                output_filename = os.path.join(
                    this_out_dir, inversed, 'cantor_{}.png'.format(i)
                )
                resize_fac /= 3
                plt.imsave(
                    output_filename,
                    to_save,
                    cmap='Greys_r'
                )

                res = mutate(res)


if __name__ == '__main__':
    main()
