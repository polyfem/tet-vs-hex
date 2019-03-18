import os
import json
import glob
import subprocess
import tempfile
import numpy as np

if __name__ == '__main__':
    polyfem_exe = "/users/teseo/Documents/scuola/polyfem/polyfem/bin_rel/PolyFEM_bin"
    out_folder = "results"

    discr_orders = [1, 2]
    fs = -np.arange(0.1, 2.1, 0.1)
    # fs = [-1]

    # discr_orders = [2]
    # fs = [-0.1]

    exts = ["mesh", "HYBRID"]

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    with open("bar.json", 'r') as f:
        json_data = json.load(f)

    for ext in exts:
        for mesh in glob.glob(os.path.join(folder_path, "*." + ext)):
            basename = os.path.splitext(os.path.basename(mesh))[0]

            bc = os.path.join(current_folder, folder_path, basename + ".txt")
            mesh = os.path.join(current_folder, mesh)

            json_data["mesh"] = mesh
            # json_data["bc_tag"] = bc

            for discr_order in discr_orders:
                for f in fs:
                    json_data["discr_order"] = discr_order
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
