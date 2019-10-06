import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = os.path.join(os.environ["POLYFEM_BIN_DIR"], "PolyFEM_bin")
    out_folder = "err"
    refs = [0, 1]

    p2s = [ [], []
        # ["square_beam.off_1.mesh", "square_beam.off_10.mesh", "square_beam.off_20.mesh", "square_beam.off_5.mesh", "square_beam.off_50.mesh", "square_beam.off_6.mesh", "square_beam.off_7.mesh", "square_beam.off_8.mesh", "square_beam.off_9.mesh"],
        # ["square_beam.off_1.mesh", "square_beam.off_5.mesh", "square_beam.off_6.mesh", "square_beam.off_7.mesh", "square_beam.off_8.mesh", "square_beam.off_9.mesh", "square_beam.off_10.mesh"]
    ]
    q1s = [[], ["square_beam.off_10.HYBRID"]
        # ["square_beam.off_1.HYBRID", "square_beam.off_10.HYBRID", "square_beam.off_20.HYBRID", "square_beam.off_5.HYBRID", "square_beam.off_50.HYBRID", "square_beam.off_6.HYBRID", "square_beam.off_7.HYBRID", "square_beam.off_8.HYBRID", "square_beam.off_9.HYBRID"],
        # ["square_beam.off_1.HYBRID", "square_beam.off_5.HYBRID", "square_beam.off_6.HYBRID", "square_beam.off_7.HYBRID", "square_beam.off_8.HYBRID", "square_beam.off_9.HYBRID", "square_beam.off_10.HYBRID"]
    ]
    splines = [ [], []
        # ["spline_square_beam.off_1.HYBRID", "spline_square_beam.off_10.HYBRID", "spline_square_beam.off_20.HYBRID", "spline_square_beam.off_5.HYBRID", "spline_square_beam.off_50.HYBRID", "spline_square_beam.off_6.HYBRID", "spline_square_beam.off_7.HYBRID", "spline_square_beam.off_8.HYBRID", "spline_square_beam.off_9.HYBRID"],
        # ["spline_square_beam.off_1.HYBRID", "spline_square_beam.off_5.HYBRID", "spline_square_beam.off_6.HYBRID", "spline_square_beam.off_7.HYBRID", "spline_square_beam.off_8.HYBRID", "spline_square_beam.off_9.HYBRID", "spline_square_beam.off_10.HYBRID"]
    ]

    n_runs = 10

    folder_path = "meshes"
    current_folder = os.getcwd()

    with open("error.json", 'r') as f:
        json_data = json.load(f)

    for run in range(n_runs):
        run_f = "run_{}".format(run)
        # os.mkdir(os.path.join(current_folder, out_folder, run_f))

        for n_refs in refs:
            p2 = p2s[n_refs]
            q1 = q1s[n_refs]
            spline = splines[n_refs]

            json_data["n_refs"] = n_refs
            print("------------------")
            print("P2")
            print("------------------")
            for mesh_name in p2:
                mesh = os.path.join("meshes", mesh_name)
                basename = os.path.splitext(os.path.basename(mesh))[0].replace("square_beam.off_", "")
                mesh = os.path.join(current_folder, mesh)

                json_data["mesh"] = mesh
                json_data["discr_order"] = 2
                json_data["use_spline"] = False
                json_data["output"] = os.path.join(current_folder, out_folder, run_f, "P2_" + basename + "_" + str(n_refs) + ".json")

                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                    with open(tmp_json.name, 'w') as f:
                        f.write(json.dumps(json_data, indent=4))

                    args = [polyfem_exe,
                            '--json', tmp_json.name,
                            '--cmd']

                    subprocess.run(args)

            #######################################################################
            print("------------------")
            print("Q1")
            print("------------------")
            for mesh_name in q1:
                mesh = os.path.join("matching_error", mesh_name)
                basename = os.path.splitext(os.path.basename(mesh))[0].replace("square_beam.off_", "")
                mesh = os.path.join(current_folder, mesh)

                json_data["mesh"] = mesh
                json_data["discr_order"] = 1
                json_data["use_spline"] = False
                json_data["output"] = os.path.join(current_folder, out_folder, run_f, "Q1_" + basename + "_" + str(n_refs) + ".json")

                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                    with open(tmp_json.name, 'w') as f:
                        f.write(json.dumps(json_data, indent=4))

                    args = [polyfem_exe,
                            '--json', tmp_json.name,
                            '--cmd']

                    subprocess.run(args)

            # #######################################################################
            print("------------------")
            print("spline")
            print("------------------")
            for mesh_name in spline:
                mesh = os.path.join("matching_error", mesh_name)
                basename = os.path.splitext(os.path.basename(mesh))[0].replace("spline_square_beam.off_", "")
                mesh = os.path.join(current_folder, mesh)

                json_data["mesh"] = mesh
                json_data["discr_order"] = 1
                json_data["use_spline"] = True
                json_data["output"] = os.path.join(current_folder, out_folder, run_f, "spline_" + basename + "_" + str(n_refs) + ".json")

                with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
                    with open(tmp_json.name, 'w') as f:
                        f.write(json.dumps(json_data, indent=4))

                    args = [polyfem_exe,
                            '--json', tmp_json.name,
                            '--cmd']

                    subprocess.run(args)
