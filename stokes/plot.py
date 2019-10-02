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


def plot(xx, yy, name, pos):
    n = int(len(xx)/3)
    x, y = zip(*sorted(zip(xx, yy))[:n])

    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name="{} {}".format(name, pos),
        line=dict(color=(colors[name]), dash='solid' if name == "Q2" else 'dash'),
    )

    return trace


def load(folder, fname):
    csv_name = os.path.join(folder, "{}.csv".format(fname))
    data = pd.read_csv(csv_name)

    x = np.array(data["arc_length"])
    y = np.array(data["solution:1"])

    return x, y


if __name__ == '__main__':
    root = "data"
    data = {
        "q50": ["Q2", "0.5"], "t50": ["P2", "0.5"],
        "q05": ["Q2", "0.05"], "t05": ["P2", "0.05"],
        "q01": ["Q2", "0.01"], "t01": ["P2", "0.01"]
        }
    output = "stokes"

    trace = []

    for out_f in data:
        x, y = load(root, out_f)
        trace.append(plot(x, y, data[out_f][0], data[out_f][1]))

    layout = go.Layout(
        legend=dict(x=0.6, y=0.87),
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
            title="Y-velocity",
            # title="Error",
            # type='log',

            tickformat='.0e',
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
