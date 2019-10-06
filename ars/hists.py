import os
import glob
import numpy as np
import pandas as pd

import plotly.graph_objs as go
import plotly.offline as plotly

colors = {
    'tet': 'rgb(9, 132, 227)', 'P1': 'rgb(9, 132, 227)', 'P2': 'rgb(108, 92, 231)',
    'hex': 'rgb(225, 112, 85)', 'Q1': 'rgb(225, 112, 85)', 'Q2': 'rgb(214, 48, 49)'}


use_logs = [
    True, False, False
]

ranges = [
    (3, 500),
    (3, 50),
    (0.6, 4)
]

steps = [
    (0.05, 10),
    (0.05, 1),
    (0.01, 0.05),
]


def plot(data, key):
    trace = []

    n = -1

    use_log = use_logs[key]

    index = 0 if use_log else 1

    mmax = ranges[key][index]
    step = steps[key][index]

    for k in data:
        v = data[k][key]
        if n == -1:
            n = len(v)
        else:
            assert(n == len(v))

        v = np.sqrt(v)
        if use_log:
            v = np.log10(v)

        v[v >= mmax] = mmax

        hist = go.Histogram(
            x = v,
            histnorm='percent',
            name = k,
            xbins=dict(  # bins used for histogram
                start=0,
                end=mmax,
                size=step
            ),
            marker=dict(color=colors[k])
        )

        trace.append(hist)

    return trace



def load(prefix):
    res = {}
    for suffix in ["tet", "hex"]:
        ext = "csv" if suffix == "tet" else "txt"

        data = pd.read_csv("{}_{}.{}".format(prefix, suffix, ext), delim_whitespace=suffix=="hex")
        mmin = data["min"].values
        mmax = data["max"].values
        avg = data["avg"].values

        res[suffix] = (mmin, mmax, avg)

    return res


if __name__ == '__main__':
    keys = {"min": 0, "max": 1, "avg": 2}

    # prefix = "10k"
    prefix = "hexalab"
    name = "avg"

    key = keys[name]
    output = "{}_{}".format(prefix, name)

    data = load(prefix)

    layout = go.Layout(
        legend=dict(x=0.81, y=0.81),
        xaxis=dict(
            title="Aspect ratio",
            exponentformat='power',
            showticksuffix='all',
            showtickprefix='all',
            showexponent='all',
            # autotick=True,
            nticks=5,
            tickfont=dict(
                size=16
            ),
            tickmode='array',
            # tickvals=[0, 0.5, 1, 1.5, 2, 2.5],
            # ticktext=['0', '', '1', '', '1e2', '']
        ),
        yaxis=dict(
            title="Percentage",
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
        bargap=0.1,
        bargroupgap=0,
        hovermode='closest'
    )

    plot_data = plot(data, key)

    fig = go.Figure(data=plot_data, layout=layout)



    if output is not None:
        plotly.plot(fig, image="svg", image_filename=output)
    else:
        plotly.plot(fig)
