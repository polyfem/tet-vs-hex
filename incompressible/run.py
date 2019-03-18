import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = "/users/teseo/Documents/scuola/polyfem/polyfem/bin_rel/PolyFEM_bin"
    vtu_folder = "vtu"
    json_folder = "out"

    discr_orders = [1, 2]
    exts = ["obj"]

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    E = 0.1
    nus = [0.9, 0.99, 0.999, 0.9999]

    with open("run.json", 'r') as f:
        json_data = json.load(f)

    for ext in exts:
        for mesh in glob.glob(os.path.join(folder_path, "*." + ext)):
            basename = os.path.splitext(os.path.basename(mesh))[0]
            title = "P" if basename.find("quad") == -1 else "Q"
            json_data["n_refs"] = 0 if basename.find("quad") == -1 else 6
            # print(json_data["n_refs"])

            mesh = os.path.join(current_folder, mesh)
            json_data["mesh"] = mesh

            for nu in nus:
                json_data["params"]["E"] = E
                json_data["params"]["nu"] = nu
                json_data["problem_params"]["use_mixed_formulation"] = False

                for discr_order in discr_orders:
                    json_data["discr_order"] = discr_order
                    json_data["output"] = os.path.join(current_folder, json_folder, title + str(discr_order) + "_nu" + str(nu) + ".json")
                    json_data["export"]["vis_mesh"] = os.path.join(current_folder, vtu_folder, title + str(discr_order) + "_nu" + str(nu) + ".vtu")

                    with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                        with open(tmp_json.name, 'w') as f:
                            f.write(json.dumps(json_data, indent=4))

                        args = [polyfem_exe,
                                '--json', tmp_json.name,
                                '--cmd',
                                '--log_level', '1']

                        subprocess.run(args)

                json_data["problem_params"]["use_mixed_formulation"] = True
                json_data["discr_order"] = 2
                json_data["output"] = os.path.join(current_folder, json_folder, title + "M_nu" + str(nu) + ".json")
                json_data["export"]["vis_mesh"] = os.path.join(current_folder, vtu_folder, title + "M_nu" + str(nu) + ".vtu")

                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                    with open(tmp_json.name, 'w') as f:
                        f.write(json.dumps(json_data, indent=4))

                    args = [polyfem_exe,
                            '--json', tmp_json.name,
                            '--cmd',
                            '--log_level', '1']

                    subprocess.run(args)
