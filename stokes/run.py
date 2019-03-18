import os
import json
import glob
# import polyfempy

import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = "/users/teseo/Documents/scuola/polyfem/polyfem/bin_rel/PolyFEM_bin"
    out_folder = "results"

    discr_orders = [2]

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    with open("experiment.json", 'r') as f:
        json_data = json.load(f)

    # solver = polyfempy.Solver()
    # solver.set_log_level(0)

    for mesh in glob.glob(os.path.join(folder_path, "*.obj")):
        basename = os.path.splitext(os.path.basename(mesh))[0]
        mesh = os.path.join(current_folder, mesh)

        json_data["mesh"] = mesh
        json_data["n_refs"] = 0 if basename.find("quad") == -1 else 6

        for discr_order in discr_orders:
            json_data["discr_order"] = discr_order
            json_data["output"] = os.path.join(current_folder, out_folder, basename + "_k" + str(discr_order) + ".json")
            json_data["export"]["vis_mesh"] = os.path.join(current_folder, out_folder, basename + "_k" + str(discr_order) + ".vtu")

            # solver.load_parameters(json.dumps(json_data))
            # solver.load_mesh()
            # solver.solve()
            # solver.export_data()
            with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                with open(tmp_json.name, 'w') as f:
                    f.write(json.dumps(json_data, indent=4))

                args = [polyfem_exe,
                        '--json', tmp_json.name,
                        '--cmd',
                        '--log_level', '1']

                subprocess.run(args)
