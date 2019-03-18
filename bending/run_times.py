import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = "/users/teseo/Documents/scuola/polyfem/cpp/bin_rel/PolyFEM_bin"
    out_folder = "times"
    folder_path = "meshes"

    discr_orders = [1, 2]
    force = -1

    exts = ["mesh", "HYBRID"]
    folder_paths = ["square", "rail", "circle"]

    n_runs = 10

    current_folder = cwd = os.getcwd()

    with open("bar.json", 'r') as f:
        json_data = json.load(f)

    json_data["problem_params"]["neumann_boundary"][0]["value"][1] = force

    for ext in exts:
        for mesh in glob.glob(os.path.join(folder_path, "*." + ext)):
            basename = os.path.splitext(os.path.basename(mesh))[0]

            # bc = os.path.join(current_folder, folder_path, basename + ".txt")
            mesh = os.path.join(current_folder, mesh)

            json_data["mesh"] = mesh
            # json_data["bc_tag"] = bc

            for discr_order in discr_orders:
                json_data["discr_order"] = discr_order
                for i in range(0, n_runs):
                    json_data["output"] = os.path.join(current_folder, out_folder, basename + "_k" + str(discr_order) + "_r" + str(i + 1) + ".json")

                    with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                        with open(tmp_json.name, 'w') as f:
                            f.write(json.dumps(json_data, indent=4))

                        args = [polyfem_exe,
                                '--json', tmp_json.name,
                                '--cmd']

                        subprocess.run(args)
