import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = os.path.join(os.environ["POLYFEM_BIN_DIR"], "PolyFEM_bin")
    vtu_folder = "vtu"
    json_folder = "out"

    discr_orders = [1, 2]
    time_steps = 40
    tend = 0.5
    exts = ["obj"]

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    with open("run.json", 'r') as f:
        json_data = json.load(f)

    json_data["time_steps"] = time_steps
    json_data["tend"] = tend

    for ext in exts:
        for mesh in glob.glob(os.path.join(folder_path, "*." + ext)):
            basename = os.path.splitext(os.path.basename(mesh))[0]
            print(basename, "\n-----------")
            title = "P" if basename.find("quad") == -1 else "Q"
            json_data["n_refs"] = 0 if basename.find("quad") == -1 else 6
            # json_data["n_refs"] = 0 if basename.find("quad") == -1 else 3
            print(json_data["n_refs"])

            mesh = os.path.join(current_folder, mesh)
            json_data["mesh"] = mesh

            for discr_order in discr_orders:
                json_data["discr_order"] = discr_order
                json_data["output"] = os.path.join(current_folder, json_folder, title + str(discr_order) + ".json")

                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                    with open(tmp_json.name, 'w') as f:
                        f.write(json.dumps(json_data, indent=4))

                    args = [polyfem_exe,
                            '--json', tmp_json.name,
                            '--cmd',
                            '--log_level', '1']

                    subprocess.run(args)

                for s in range(time_steps+1):
                    os.rename(
                        os.path.join(current_folder, "step_{}.vtu".format(s)),
                        os.path.join(current_folder, vtu_folder, "{}{}_step_{:02d}.vtu".format(title, discr_order, s)))
                    os.rename(
                        os.path.join(current_folder, "step_{}.obj".format(s)),
                        os.path.join(current_folder, vtu_folder, "{}{}_step_{:02d}.obj".format(title, discr_order, s)))

