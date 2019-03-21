import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = os.path.join(os.environ["POLYFEM_BIN_DIR"], "PolyFEM_bin")
    out_folder = "results"

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    discr_orders = [1, 2]

    with open("plane_hole.json", 'r') as f:
        json_data = json.load(f)

    for mesh in glob.glob(os.path.join(folder_path, "*.obj")):
        basename = os.path.splitext(os.path.basename(mesh))[0]

        mesh = os.path.join(current_folder, mesh)
        json_data["mesh"] = mesh

        for discr_order in discr_orders:
            json_data["discr_order"] = discr_order
            json_data["output"] = os.path.join(current_folder, out_folder, "out_" + basename + "_k" + str(discr_order) + ".json")
            json_data["export"]["vis_mesh"] = os.path.join(current_folder, out_folder, "sol_" + basename + "_k" + str(discr_order) + ".vtu")

            with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                with open(tmp_json.name, 'w') as f:
                    f.write(json.dumps(json_data, indent=4))

                args = [polyfem_exe,
                        '--json', tmp_json.name,
                        '--cmd']

                subprocess.run(args)
