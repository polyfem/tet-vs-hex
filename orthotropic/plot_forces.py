import os
import glob
import numpy as np
import json

import plotly.graph_objs as go
import plotly.offline as plotly

colors = {'P1': 'rgb(9, 132, 227)', 'P2': 'rgb(108, 92, 231)', 'Q1': 'rgb(225, 112, 85)', 'Q2': 'rgb(214, 48, 49)'}
marker_shapes = {'P1': 'circle', 'P2': 'circle', 'Q1': 'star', 'Q2': 'star'}
marker_sizes = {'P1': 6, 'P2': 6, 'Q1': 10, 'Q2': 10}


def plot(f, k, slope, name):
    if len(f) <= 0 or len(k) <= 0:
        return []

    x, y = zip(*sorted(zip(f, k))[:])
    y = np.absolute(y - np.asarray(x)*slope)

    w = np.polyfit(x[:], y[:], 1)

    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name="{} {:.2e}".format(name, w[0]),
        line=dict(color=(colors[name])),
        marker=dict(symbol=marker_shapes[name], size=marker_sizes[name])
    )

    return [trace]


def plot_exact(f, kk):
    mmin = np.amin(f)
    mmax = np.amax(f)

    x = [mmin, mmax]
    y = [mmin * kk, mmax * kk]

    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        showlegend=False,
        line=dict(color='rgb(178, 190, 195)', dash='dash')
    )

    return [trace]


def load(mesh_name):
    k1 = []
    f1 = []
    k2 = []
    f2 = []

    for json_file in glob.glob(os.path.join(os.path.dirname(__file__), out_folder, mesh_name + "_k*.json")):
        with open(json_file, 'r') as f:
            json_data = json.load(f)

        k = json_data["discr_order"]
        disp = json_data["sol_min"][1]

        f = -json_data["args"]["problem_params"]["neumann_boundary"][0]["value"][1]
        if f == 0:
            print(json_file)

        if k == 1:
            k1.append(disp)
            f1.append(f)
        else:
            k2.append(disp)
            f2.append(f)

    return f1, k1, f2, k2


if __name__ == '__main__':
    out_folder = "results"
    output = "ortho"

    tri_name = "square_beam"
    hex_name = "square_beam_h"
    kk = -10.601655711409355 / 0.00002


    tf1, tk1, tf2, tk2 = load(tri_name)
    hf1, hk1, hf2, hk2 = load(hex_name)

    layout = go.Layout(
        legend=dict(x=0.01, y=0.81),
        xaxis=dict(
            title="Force",
            exponentformat='power',
            showticksuffix='all',
            showtickprefix='all',
            showexponent='all',
            # autotick=True,
            nticks=5,
            tickfont=dict(
                size=16
            )
        ),
        yaxis=dict(
            title="Error",
            # tickformat='.1e',
            exponentformat='power',
            ticks='',
            # tick0=0,
            # dtick=1,
            # tickangle=-45,
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

    data.extend(plot(hf1, hk1, kk, "Q1"))
    data.extend(plot(hf2, hk2, kk, "Q2"))

    data.extend(plot(tf1, tk1, kk, "P1"))
    data.extend(plot(tf2, tk2, kk, "P2"))

    # data.extend(plot_exact(tf1, kk))

    fig = go.Figure(data=data, layout=layout)
    if output is not None:
        plotly.plot(fig, image="svg", image_filename=output)
    else:
        plotly.plot(fig)
