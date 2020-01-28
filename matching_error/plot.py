import os
import json
import glob
import pandas as pd
from pandas.io.json import json_normalize
import numpy as np
import pickle

import plotly.graph_objs as go
import plotly.offline as plotly

colors = {'P1': 'rgb(9, 132, 227)', 'P2': 'rgb(108, 92, 231)', 'Q1': 'rgb(225, 112, 85)', 'Q2': 'rgb(214, 48, 49)', 'SR': 'rgb(253, 203, 110)', 'Q2R': 'rgb(255, 234, 167)', 'S': 'rgb(250, 177, 160)', 'Spline': 'rgb(45, 52, 54)'}
marker_shapes = {'P1': 'circle', 'P2': 'circle', 'Q1': 'star', 'Q2': 'star','Q2R': 'star','SR': 'star','S': 'star', 'Spline': 'square'}
marker_sizes = {'P1': 6, 'P2': 6, 'Q1': 10, 'Q2': 10, 'Q2R': 10, 'SR': 10, 'S': 10, 'Spline': 6}


def plot(k, ratio, name):
    if len(k) <=0:
        return []

    x = []

    for v in k[0]["sol_min"].values:
        x.append(abs(v[1] - ratio * 2))

    y = np.zeros(k[0]["time_solving"].values.shape)

    for e in k:
        y += e["time_building_basis"].values + e["time_assembling_stiffness_mat"].values + e["time_solving"].values
        # y += e["time_solving"].values
        # y += e["solver_info.mem_total_peak"].values

    y /= len(k)

    if name == "SR":
        x, y = zip(*sorted(zip(x, y))[2:-2])
    #     # x = x[2:]
    #     # y = y[2:]
    else:
        x, y = zip(*sorted(zip(x, y))[2:])

    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name=name,
        line=dict(color=(colors[name])),
        marker=dict(symbol=marker_shapes[name], size=marker_sizes[name])
    )

    return [trace]


def load(mesh_name, first, name, data_folder):
    k1 = []
    k2 = []

    pickle_path = os.path.join(data_folder, name)
    if os.path.isfile(pickle_path):
        with open(pickle_path, "rb") as fp:
            return pickle.load(fp)



    for r in range(10):
        k1t = pd.DataFrame()
        k2t = pd.DataFrame()

        for json_file in glob.glob(os.path.join(out_folder, "run_{}".format(r), mesh_name + "*.json")):
            with open(json_file, 'r') as f:
                json_data = json.load(f)

            if json_data is None:
                print(json_file)
            k = json_data["discr_order"]

            tmp = json_normalize(json_data)

            if k == 1:
                if k1t.empty:
                    k1t = tmp
                else:
                    k1t = pd.concat([k1t, tmp])
            else:
                if k2t.empty:
                    k2t = tmp
                else:
                    k2t = pd.concat([k2t, tmp])
        k1.append(k1t)
        k2.append(k2t)

    tmp = k1 if first else k2

    with open(pickle_path, "wb") as fp:
        pickle.dump(tmp, fp)

    return tmp


if __name__ == '__main__':
    out_folder = "err"
    data_folder = "data"

    tri_name = "P2_"
    hex_name = "Q1_"
    reduced_name = "Q2R_"
    q2_name = "Q2_"
    spline_name = "spline_"
    serendipity_r = "SR_"
    serendipity = "S_"

    # using dense P4 solution
    ratio = -0.09694505138106606 / 2


    output = None #"P2_Q1_S"

    tk2 = load(tri_name, False, "tk2.pkl", data_folder)
    hk1 = load(hex_name, True, "hk1.pkl", data_folder)
    hs = load(spline_name, True, "hs.pkl", data_folder)
    reduced = load(reduced_name, False, "reduced.pkl", data_folder)
    q2 = load(q2_name, False, "q2.pkl", data_folder)
    sr = load(serendipity_r, False, "sr.pkl", data_folder)
    S = load(serendipity, False, "S.pkl", data_folder)


    layout = go.Layout(
        legend=dict(x=0.9, y=0.9),
        xaxis=dict(
            title="Error",
            exponentformat='power',
            showticksuffix='all',
            showtickprefix='all',
            showexponent='all',
            # autotick=True,
            type='log',
            nticks=5,
            tickfont=dict(
                size=16
            ),
            # autorange='reversed'
        ),
        yaxis=dict(
            title="Time",
            # tickformat='.1e',
            exponentformat='power',
            ticks='',
            # tick0=0,
            # dtick=1,
            # tickangle=-45,
            type='log',
            tickfont=dict(
                size=16
            ),
            autorange=True
        ),
        font=dict(
            size=24
        ),
        hovermode='closest'
    )

    data = []
    data.extend(plot(hk1, ratio, "Q1"))
    data.extend(plot(tk2, ratio, "P2"))

    data.extend(plot(hs, ratio, "Spline"))
    # data.extend(plot(reduced, ratio, "Q2R"))
    data.extend(plot(q2, ratio, "Q2"))
    data.extend(plot(sr, ratio, "SR"))
    data.extend(plot(S, ratio, "S"))


    fig = go.Figure(data=data, layout=layout)
    if output is not None:
        plotly.plot(fig, image="svg", image_filename=output)
    else:
        plotly.plot(fig)
