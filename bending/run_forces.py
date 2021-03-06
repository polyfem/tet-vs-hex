import os
import json
import glob
import subprocess
import tempfile
import numpy as np

if __name__ == '__main__':
    polyfem_exe = os.path.join(os.environ["POLYFEM_BIN_DIR"], "PolyFEM_bin")
    # out_folder = "results"
    # folder_path = "meshes"
    # j_file = "bar.json"

    out_folder = "ar_res"
    folder_path = "ar"
    j_file = "ar.json"

    discr_orders = [1, 2]
    fs = -np.arange(0.1, 2.1, 0.1)

    exts = [".mesh", ".HYBRID"]

    nodes = {"P1": 3962, "P2": 13688, "Q1": 6077, "Q2": 43097}


    current_folder = cwd = os.getcwd()

    with open(j_file, 'r') as f:
        json_data = json.load(f)

    for ext in exts:
        for mesh in glob.glob(os.path.join(folder_path, "*" + ext)):
            print(mesh)
            basename = os.path.splitext(os.path.basename(mesh))[0]

            bc = os.path.join(current_folder, folder_path, basename + ".txt")
            mesh = os.path.join(current_folder, mesh)

            json_data["mesh"] = mesh

            key = "Q" if "HYBRID" in ext else "P"

            for discr_order in discr_orders:
                node_id = nodes[key + str(discr_order)]
                if "rail" in basename:
                    json_data["export"]["sol_at_node"] = node_id
                else:
                    json_data["export"]["sol_at_node"] = -1

                for f in fs:
                    json_data["discr_order"] = discr_order
                    if "nice" in basename:
                        f = -f
                    json_data["problem_params"]["neumann_boundary"][0]["value"][1] = f
                    json_data["output"] = os.path.join(current_folder, out_folder, basename + "_k" + str(discr_order) + "_f" + str(abs(f)) + ".json")
                    # json_data["output"] = os.path.join(current_folder, out_folder, "out_" + basename + "_k" + str(discr_order) + ".json")

                    with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                        with open(tmp_json.name, 'w') as f:
                            f.write(json.dumps(json_data, indent=4))

                        args = [polyfem_exe,
                                '--json', tmp_json.name,
                                '--cmd']

                        subprocess.run(args)
