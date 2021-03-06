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


def print_line(title, tb, ta, ts, t, e):
    string = "{}&\t{:.2e}&\t{:.2e}&\t{:.2e}&\t{:.2e}&\t{:.2e}\\\\".format(title, tb, ta, ts, t, e)
    string = string.replace("e-0", "e-")
    string = string.replace("e+0", "e")
    string = string.replace("e0", "")
    print(string)


if __name__ == '__main__':
    path = "times"
    prefixes = ["square_beam", "square_beam_h"]


    exacts = {
        "square_beam": -10.601655711409355 / 2
    }

    discrs = [1, 2]


    basis = {}
    assembly = {}
    solve = {}
    total = {}
    errors = {}

    for prefix in prefixes:
        basis[prefix] = []
        assembly[prefix] = []
        solve[prefix] = []
        total[prefix] = []
        errors[prefix] = []

    for prefix in prefixes:
        for discr in discrs:
            bb = []
            aa = []
            ss = []
            tt = []
            ee = []
            for data in glob.glob(os.path.join(path, prefix + "_k" + str(discr) + "*.json")):
                with open(data, 'r') as f:
                    json_data = json.load(f)

                    if "rail" in prefix:
                        disp = json_data["sol_at_node"][1]
                    else:
                        disp = json_data["sol_min"][1]

                    exact = exacts[prefix.replace("_h", "").replace("_nice", "")]

                    bb.append(json_data["time_building_basis"])
                    aa.append(json_data["time_assembling_stiffness_mat"])
                    ss.append(json_data["time_solving"])

                    tt.append(json_data["time_building_basis"]+json_data["time_assembling_stiffness_mat"]+json_data["time_solving"])
                    ee.append(abs(exact-disp))

            basis[prefix].append(bb)
            assembly[prefix].append(aa)
            solve[prefix].append(ss)
            total[prefix].append(tt)
            errors[prefix].append(ee)


    for i in range(0, len(prefixes), 2):
        pp = prefixes[i]
        qq = prefixes[i+1]
        print("\n\n" + pp + " " + qq + "\n")

        print("&$t_b$&\t$t_a$&\t$t_s$&\t$t$&\t$e_f$\\\\")
        print("\\hline")
        [p1b, p2b, q1b, q2b] = get_data(basis[pp], basis[qq])
        [p1a, p2a, q1a, q2a] = get_data(assembly[pp], assembly[qq])
        [p1s, p2s, q1s, q2s] = get_data(solve[pp], solve[qq])
        [p1t, p2t, q1t, q2t] = get_data(total[pp], total[qq])
        [p1e, p2e, q1e, q2e] = get_data(errors[pp], errors[qq])
        print_line("$P_1$", p1b, p1a, p1s, p1t, p1e)
        print_line("$P_2$", p2b, p2a, p2s, p2t, p2e)
        print_line("$Q_1$", q1b, q1a, q1s, q1t, q1e)
        print_line("$Q_2$", q2b, q2a, q2s, q2t, q2e)
