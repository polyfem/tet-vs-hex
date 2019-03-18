import os
import json


def get_filed(data, other, field):
    if field == "time":
        vbase = data["time_building_basis"] + data["time_assembling_stiffness_mat"]  +data["time_solving"]
        vother = other["time_building_basis"] + other["time_assembling_stiffness_mat"]  +other["time_solving"]
    elif field == "memory":
        vbase = data["solver_info"]["mem_total_peak"]
        vother = other["solver_info"]["mem_total_peak"]
    elif field == "DOF":
        vbase = round(data["num_dofs"]/3)
        vother = round(other["num_dofs"]/3)
    elif field == "error":
        vbase = abs(data["sol_min"][1] - -0.09694505138106606)
        vother = abs(other["sol_min"][1] - -0.09694505138106606)
    else:
        vbase = data[field]
        vother = other[field]

    return vbase, vother


def print_line(data, other, field, is_diag, format):
    [vbase, vother] = get_filed(data, other, field)

    if field == "time":
        vbases = "{:.2f}".format(vbase)
        vothers = "{:.2f}".format(vother)
    elif field == "memory":
        vbases = "{:,}".format(round(vbase/1024))
        vothers = "{:,}".format(round(vother/1024))
        # vbases = "{:,}".format(round(vbase))
        # vothers = "{:,}".format(round(vother))
    elif field == "DOF":
        vbases = "{:,}".format(vbase)
        vothers = "{:,}".format(vother)
    elif field == "error":
        vbases = "{:.2e}".format(vbase)
        vothers = "{:.2e}".format(vother)
    else:
        vbases = "{}".format(vbase)
        vothers = "{}".format(vother)

    if(is_diag):
        string = "\\diagcol{" + vbases + "~/~" + vothers + "}"
    else:
        if vbase < vother:
            string = "\\goodcol{" + vbases + "}~/~" + vothers
        else:
            string = vbases + "~/~\\goodcol{" + vothers + "}"

    return string


if __name__ == '__main__':
    path = "results"
    discrs = [1, 2, 3]

    keys = ["time", "memory", "DOF", "error"]

    print("\\begin{tabular}{lr|cccc}")
    print("&&time (s)&\tmemory (MB)&\tDOF&\terror\\\\")
    for kk in discrs:
        p = 2 if kk == 3 else kk
        q = 1 if kk == 3 else kk

        with open(os.path.join(path, "out_p" + str(p) + ".json"), 'r') as f:
            data = json.load(f)

        with open(os.path.join(path, "out_same_dof_p" + str(kk) + ".json"), 'r') as f:
            same_dof = json.load(f)

        with open(os.path.join(path, "out_same_err_p" + str(kk) + ".json"), 'r') as f:
            same_err = json.load(f)

        with open(os.path.join(path, "out_same_mem_p" + str(kk) + ".json"), 'r') as f:
            same_mem = json.load(f)

        with open(os.path.join(path, "out_same_time_p" + str(kk) + ".json"), 'r') as f:
            same_time = json.load(f)

        print("\\hline")
        print("\\multirow{" + ("4" if p == 1 else "3") + "}{*}{\\rotatebox{90}{$P_"+str(p)+"$/$Q_"+str(q)+"$}}")

        for k1 in keys:
            print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
            print("&" + k1 + "&")
            if k1 == "time":
                other = same_time
            elif k1 == "memory":
                other = same_mem
            elif k1 == "DOF":
                other = same_dof
            else:
                other = same_err
            for k2 in keys:
                print(print_line(data, other, k2, k1 == k2, ":") + ("\\\\" if k2 == keys[-1] else "&"))

        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

    print("\\end{tabular}")
