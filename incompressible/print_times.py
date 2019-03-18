import os
import json
import glob
import numpy as np


def get_data(p, q):
    p1 = p[0]
    p2 = p[1]

    q1 = q[0]
    q2 = q[1]

    p1 = np.mean(p1)
    p2 = np.mean(p2)
    q1 = np.mean(q1)
    q2 = np.mean(q2)

    return p1, p2, q1, q2


def print_line(title, tb, ta, ts, t):
    string = "{}&\t{:.2e}&\t{:.2e}&\t{:.2e}&\t{:.2e}\\\\".format(title, tb, ta, ts, t)
    string = string.replace("e-0", "e-")
    string = string.replace("e+0", "e")
    string = string.replace("e0", "")
    print(string)


if __name__ == '__main__':
    path = "out"
    prefixes = ["P1", "P2", "PM", "Q1", "Q2", "QM"]


    basis = {}
    assembly = {}
    solve = {}
    total = {}

    for prefix in prefixes:
        basis[prefix] = []
        assembly[prefix] = []
        solve[prefix] = []
        total[prefix] = []

    for prefix in prefixes:
        total_time = 0
        count = 0
        for data in glob.glob(os.path.join(path, prefix + "*.json")):
            with open(data, 'r') as f:
                json_data = json.load(f)

                time = json_data["time_building_basis"] + json_data["time_assembling_stiffness_mat"] + json_data["time_solving"]
                total_time += time
                count += 1

        print(prefix)
        print(round(total_time / count*100)/100)
