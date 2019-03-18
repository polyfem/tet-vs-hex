import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = "/Users/teseo/Documents/scuola/polyfem/polyfem/bin_rel.nosync/PolyFEM_bin"
    out_folder = "results"
    vtu_folder = "vtu"

    discr_orders = [1, 2]

    exts = ["mesh", "HYBRID"]

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    with open("bar.json", 'r') as f:
        json_data = json.load(f)

    for ext in exts:
        n_refs = 0 if ext == "mesh" else 4
        name = "p" if ext == "mesh" else "q"
        json_data["n_refs"] = n_refs

        for mesh in glob.glob(os.path.join(folder_path, "*." + ext)):
            basename = os.path.splitext(os.path.basename(mesh))[0]
            mesh = os.path.join(current_folder, mesh)

            json_data["mesh"] = mesh

            for discr_order in discr_orders:
                json_data["discr_order"] = discr_order
                json_data["output"] =             os.path.join(current_folder, out_folder, "out_" + basename + "_" + name + str(discr_order) + ".json")
                json_data["export"]["vis_mesh"] = os.path.join(current_folder, vtu_folder, "out_" + basename + "_" + name + str(discr_order) + ".vtu")


                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                    with open(tmp_json.name, 'w') as f:
                        f.write(json.dumps(json_data, indent=4))

                    args = [polyfem_exe,
                            '--json', tmp_json.name,
                            '--cmd']

                    subprocess.run(args)
