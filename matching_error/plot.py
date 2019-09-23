import os
import json
import glob
import pandas as pd
from pandas.io.json import json_normalize

import plotly.graph_objs as go
import plotly.offline as plotly

colors = {'P1': 'rgb(9, 132, 227)', 'P2': 'rgb(108, 92, 231)', 'Q1': 'rgb(225, 112, 85)', 'Q2': 'rgb(214, 48, 49)', 'Spline': 'rgb(45, 52, 54)'}
marker_shapes = {'P1': 'circle', 'P2': 'circle', 'Q1': 'star', 'Q2': 'star'}
marker_sizes = {'P1': 6, 'P2': 6, 'Q1': 10, 'Q2': 10}


def plot(k, ratio, name):
    if k.empty:
        return []

    x = []

    for v in k["sol_min"].values:
        x.append(abs(v[1] - ratio * 2))

    y = k["time_building_basis"].values + k["time_assembling_stiffness_mat"].values + k["time_solving"].values
    # y = k["time_solving"].values
    # y = k["solver_info.mem_total_peak"].values

    if name == "Q1":
        x, y = zip(*sorted(zip(x, y))[2:])
        # x = x[2:]
        # y = y[2:]
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


def load(mesh_name):

    k1 = pd.DataFrame()
    k2 = pd.DataFrame()

    for json_file in glob.glob(os.path.join(out_folder, mesh_name + "*.json")):
        with open(json_file, 'r') as f:
            json_data = json.load(f)

        k = json_data["discr_order"]

        tmp = json_normalize(json_data)

        if k == 1:
            if k1.empty:
                k1 = tmp
            else:
                k1 = pd.concat([k1, tmp])
        else:
            if k2.empty:
                k2 = tmp
            else:
                k2 = pd.concat([k2, tmp])

    return k1, k2


if __name__ == '__main__':
    out_folder = "err"

    tri_name = "P2_"
    hex_name = "Q1_"
    spline_name = "spline_"

    # using dense P4 solution
    ratio = -0.09694505138106606 / 2


    output = "P2_Q1"

    _, tk2 = load(tri_name)
    hk1, _ = load(hex_name)
    hs, _ = load(spline_name)

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


    fig = go.Figure(data=data, layout=layout)
    if output is not None:
        plotly.plot(fig, image="svg", image_filename=output)
    else:
        plotly.plot(fig)
