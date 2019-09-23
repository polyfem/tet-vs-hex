import numpy as np
import igl
import meshplot as mp
import wildmeshing as wm


mp.offline()

v=np.array([
    [-10., -0.5, -50],
    [-10., 0.5, -50],
    [10., 0.5, -50],
    [10., -0.5, -50],
    #
    [-10., -0.5, 50],
    [-10., 0.5, 50],
    [10., 0.5, 50],
    [10., -0.5, 50]
    ])

f = np.array([
    [0, 1, 2],
    [2, 3, 0],

    [4, 6, 5],
    [6, 4, 7],

    [2, 6, 7],
    [3, 2, 7],

    [1, 5, 6],
    [1, 6, 2],

    [1, 4, 5],
    [4, 1, 0],

    [0, 7, 4],
    [7, 0, 3]
])

# igl.write_triangle_mesh("bbb.obj", v, f)
# p = mp.plot(v, f, shading={"wireframe": True, "point_size": 5}, return_plot=True, filename="plot.html")


# wm.tetrahedralize("bbb.obj", "test.mesh", edge_length_r=0.0263)

n_v = -1
index = -1
with open("test.mesh", "r") as in_file:
    with open("test_snap.mesh", "w") as out_file:
        for line in in_file:
            if n_v == -2:
                n_v = int(line)
                print(n_v)
            if "Vertices" in line:
                n_v = -2

            if index < n_v and index >= 0:
                nbrs = line.split(' ')
                assert(len(nbrs) == 4)

                x = float(nbrs[0])
                y = float(nbrs[1])
                z = float(nbrs[2])

                if abs(x-10) < 1e-1:
                    x = 10
                if abs(x+10) < 1e-1:
                    x = -10

                if abs(y-0.5) < 1e-1:
                    y = 0.5
                if abs(y+0.5) < 1e-1:
                    y = -0.5
                if abs(z-50) < 1e-1:
                    z = 50
                if abs(z+50) < 1e-1:
                    z = -50

                line = "{} {} {} {}".format(x, y, z, nbrs[3])

            out_file.write(line)

            if n_v > 0:
                index += 1
