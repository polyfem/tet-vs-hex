import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = "/users/teseo/Documents/scuola/polyfem/polyfem/bin_rel/PolyFEM_bin"
    out_folder = "results"

    discr_orders = [2]

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    with open("beam.json", 'r') as f:
        json_data = json.load(f)

    for discr_order in discr_orders:
        mesh = os.path.join(current_folder, folder_path + "/mesh.mesh")
        json_data["mesh"] = mesh
        json_data["discr_order"] = 1 if discr_order == 3 else discr_order
        json_data["output"] = os.path.join(current_folder, out_folder, "out_p" + str(discr_order) + ".json")

        # with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
        #     with open(tmp_json.name, 'w') as f:
        #         f.write(json.dumps(json_data, indent=4))

        #     args = [polyfem_exe,
        #             '--json', tmp_json.name,
        #             '--cmd']

        #     subprocess.run(args)

        for mesh in glob.glob(os.path.join(folder_path, "*_p" + str(discr_order) + ".HYBRID")):

            basename = os.path.splitext(os.path.basename(mesh))[0]
            mesh = os.path.join(current_folder, mesh)

            print("\n\n----------------------------")
            print(basename)
            print("----------------------------")

            json_data["mesh"] = mesh
            json_data["output"] = os.path.join(current_folder, out_folder, "out_" + basename + ".json")


            with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                with open(tmp_json.name, 'w') as f:
                    f.write(json.dumps(json_data, indent=4))

                args = [polyfem_exe,
                        '--json', tmp_json.name,
                        '--cmd']

                subprocess.run(args)
