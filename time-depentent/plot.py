import os
import glob
import numpy as np
import json
import pandas as pd

import plotly.graph_objs as go
import plotly.offline as plotly


colors = {'P1': 'rgb(9, 132, 227)', 'P2': 'rgb(108, 92, 231)', 'Q1': 'rgb(225, 112, 85)', 'Q2': 'rgb(214, 48, 49)'}
marker_shapes = {'P1': 'circle', 'P2': 'circle', 'Q1': 'star', 'Q2': 'star'}
marker_sizes = {'P1': 6, 'P2': 6, 'Q1': 10, 'Q2': 10}


def plot(t, disp, name, suffix):
    x, y = zip(*sorted(zip(t, disp))[:])

    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines+markers',
        name="{} {}".format(name, suffix),
        line=dict(color=(colors[name]), dash='solid' if suffix == "coarse" else "dash"),
        marker=dict(symbol=marker_shapes[name], size=marker_sizes[name]* (1 if suffix == "coarse" else 0))
    )

    return trace



def load(name, folder, tend):
    csv_name = os.path.join(folder, "{}.csv".format(name))
    data = pd.read_csv(csv_name)
    t = np.array(data["Time"])
    t = t/np.max(t)*tend
    disp = np.array(data["max(solution (0))"])

    return name, t, disp


if __name__ == '__main__':
    out_folders = {"vtu": "fine", "vtu_coarse": "coarse"}
    # out_folders = {"vtu_coarse": "coarse"}
    tend = 0.5
    output = "plot"

    trace = []
    for out_f in out_folders:
        for k in colors:
            n, t, disp = load(k, out_f, tend)
            # err = np.abs(dispp1 - exact)

            trace.append(plot(t, disp, n, out_folders[out_f]))

    layout = go.Layout(
        legend=dict(x=0.1, y=0.87),
        xaxis=dict(
            title="Time",
            showticksuffix='all',
            showtickprefix='all',
            showexponent='all',
            # autotick=True,
            nticks=6,
            tickfont=dict(
                size=16
            )
        ),
        yaxis=dict(
            title="X-displacement",
            # title="Error",
            # type='log',

            # tickformat='.1e',
            exponentformat='power',
            ticks='',
            # tick0=0,
            # dtick=1,
            # tickangle=-45,
            tickfont=dict(
                size=16
            ),
            autorange=True,
        ),
        font=dict(
            size=24
        ),
        hovermode='closest'
    )

    fig = go.Figure(data=trace, layout=layout)
    if output is not None:
        plotly.plot(fig, image="svg", image_filename=output)
    else:
        plotly.plot(fig)
