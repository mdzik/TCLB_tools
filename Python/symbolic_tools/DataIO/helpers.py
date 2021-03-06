import os
import re
import numpy as np


def delete_unphysical_data_from_wall_nodes(data, n_to_strip_per_side):
    # data = np.delete(data, 0, axis=0)
    # data = np.delete(data, -1, axis=0)
    data = np.delete(data, np.s_[:n_to_strip_per_side], axis=0)
    data = np.delete(data, np.s_[-n_to_strip_per_side:], axis=0)
    return data


def peel_the_skin(some_2d_array):
    # clip the array from each side, so that both EQ and ABB scheme would have the same 'measurement' nodes
    some_2d_array = np.delete(some_2d_array, 0, axis=0)
    some_2d_array = np.delete(some_2d_array, 0, axis=1)

    # n_rows, n_columns = some_2d_array.shape
    some_2d_array = np.delete(some_2d_array, (some_2d_array.shape[0] - 1), axis=0)  # delete last row
    some_2d_array = np.delete(some_2d_array, (some_2d_array.shape[1] - 1), axis=1)  # delete last column

    return some_2d_array

def peel_the_skin_v2(some_2d_array, start, end):
    # clip the array from each side
    some_2d_array = some_2d_array[start:end, start:end]
    return some_2d_array

def get_r_from_xy(x, y, x0=0, y0=0):
    r = np.sqrt(pow(x0 - x, 2) + pow(y0 - y, 2))
    return r


def eat_dots_for_texmaker(value):
    s_value = str(value)
    s_value = re.sub(r"\.", 'o', s_value)
    return s_value


def strip_folder_name(some_folder):
    some_folder = some_folder.rstrip('0')  # remove all trailing zeros
    some_folder = some_folder.rstrip('.')
    return some_folder


def find_oldest_iteration(folder, extension='.pvti'):
    prefix = 'VTK_P00_'
    pattern = prefix.join(r"(\d{4,8})")
    iterations = []
# "batch_HotKarman_Re1000_D0_1.28e+02_nu_0.0055_U_4.30e-02_bc_HeaterDirichletTemperatureEQ_CM_HIGHER_VTK_P00_00006003"
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(extension):
                it_counter = re.findall(r"VTK_P00_(\d{4,8})", file)  # from 4 to 8 digits
                # it_counter = re.findall(r"(\d{4,8})", file)  # from 4 to 8 digits
                if len(it_counter) > 0:
                    iterations.append(it_counter[0])



    # int_iterations = [int(i) for i in iterations]
    # oldest = max(int_iterations)
    # idx = int_iterations.index(oldest)
    if not iterations:
        raise FileNotFoundError(f'Check the path: \n {folder}')

    # oldest = max(iterations)
    iterations.sort()
    oldest = iterations[-1]
    # oldest = iterations[6]
    return oldest


def get_vti_from_iteration(folder, iteration, extension='.vti', prefix='VTK_P00_'):
    pattern = f"{prefix}{iteration}{extension}"
    matched_files = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith(pattern):
                matched_files.append(file)

    if not matched_files:
        raise FileNotFoundError(f'Check the path: \n {folder}')

    if len(matched_files) > 1:
        raise Exception("More than 1 matching file")

    return matched_files[0]


def calc_mse(anal, num):
    return np.sum((anal - num) * (anal - num)) / len(anal)


def calc_L2(anal, num):
    # Eq. 4.57
    return np.sqrt(np.sum((anal - num) * (anal - num)) / np.sum(anal * anal))
