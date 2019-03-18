import os
import json
import glob
import subprocess
import tempfile

if __name__ == '__main__':
    polyfem_exe = "/users/teseo/Documents/scuola/polyfem/cpp/bin_rel/PolyFEM_bin"
    out_folder = "err"

    p2 = ["square_beam.off_1.mesh", "square_beam.off_10.mesh", "square_beam.off_20.mesh", "square_beam.off_5.mesh", "square_beam.off_50.mesh", "square_beam.off_6.mesh", "square_beam.off_7.mesh", "square_beam.off_8.mesh", "square_beam.off_9.mesh"]
    q1 = ["square_beam.off_1.HYBRID", "square_beam.off_10.HYBRID", "square_beam.off_20.HYBRID", "square_beam.off_5.HYBRID", "square_beam.off_50.HYBRID", "square_beam.off_6.HYBRID", "square_beam.off_7.HYBRID", "square_beam.off_8.HYBRID", "square_beam.off_9.HYBRID"]
    spline = ["spline_square_beam.off_1.HYBRID", "spline_square_beam.off_10.HYBRID", "spline_square_beam.off_20.HYBRID", "spline_square_beam.off_5.HYBRID", "spline_square_beam.off_50.HYBRID", "spline_square_beam.off_6.HYBRID", "spline_square_beam.off_7.HYBRID", "spline_square_beam.off_8.HYBRID", "spline_square_beam.off_9.HYBRID"]

    folder_path = "meshes"
    current_folder = cwd = os.getcwd()

    with open("error.json", 'r') as f:
        json_data = json.load(f)

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
        json_data["output"] = os.path.join(current_folder, out_folder, "P2_" + basename + ".json")

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
        json_data["output"] = os.path.join(current_folder, out_folder, "Q1_" + basename + ".json")

        with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
            with open(tmp_json.name, 'w') as f:
                f.write(json.dumps(json_data, indent=4))

            args = [polyfem_exe,
                    '--json', tmp_json.name,
                    '--cmd']

            subprocess.run(args)

    # #######################################################################
    # print("------------------")
    # print("spline")
    # print("------------------")
    # for mesh_name in spline:
    #     mesh = os.path.join("matching_error", mesh_name)
    #     basename = os.path.splitext(os.path.basename(mesh))[0].replace("spline_square_beam.off_", "")
    #     mesh = os.path.join(current_folder, mesh)

    #     json_data["mesh"] = mesh
    #     json_data["discr_order"] = 1
    #     json_data["use_spline"] = True
    #     json_data["output"] = os.path.join(current_folder, out_folder, "spline_" + basename + ".json")

    #     with tempfile.NamedTemporaryFile(suffix=".json") as tmp_json:
    #         with open(tmp_json.name, 'w') as f:
    #             f.write(json.dumps(json_data, indent=4))

    #         args = [polyfem_exe,
    #                 '--json', tmp_json.name,
    #                 '--cmd']

    #         subprocess.run(args)
