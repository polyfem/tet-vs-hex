import numpy as np
import math
import pandas as pd

import plotly.graph_objs as go
import plotly.offline as plotly

colors = {'P1': 'rgb(9, 132, 227)', 'P2': 'rgb(108, 92, 231)', 'Q1': 'rgb(225, 112, 85)', 'Q2': 'rgb(214, 48, 49)', 'Spline': 'rgb(45, 52, 54)'}
marker_shapes = {'P1': 'circle', 'P2': 'circle', 'Q1': 'star', 'Q2': 'star'}
marker_sizes = {'P1': 6, 'P2': 6, 'Q1': 10, 'Q2': 10}


def plot(data, name):
    if data.empty:
        return []

    x = data["arc_length"].values

    px = data["solution:0"].values
    py = data["solution:1"].values

    y = -np.arctan2(py, px) / math.pi * 180
    y -= 45.
    # y[0] += 45
    y = np.abs(y - x/100*90)

    x, y = zip(*sorted(zip(x, y))[20:])

    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        name=name,
        line=dict(color=(colors[name])),
        # marker=dict(symbol=marker_shapes[name], size=marker_sizes[name])
    )


    return [trace]


def plot_exact():
    m = -0.015677840125715936
    b = -0.788410994193744
    mmin = 0
    mmax = 100

    x = [mmin, mmax]
    y = [b + mmin * m, b+ mmax * m]

    trace = go.Scatter(
        x=x,
        y=y,
        mode='lines',
        showlegend=False,
        line=dict(color='rgb(178, 190, 195)', dash='dash')
    )

    return [trace]


if __name__ == '__main__':
    out_folder = "data"
    output = "plot_fine"

    p1 = pd.read_csv(out_folder + "/P1.csv")
    p2 = pd.read_csv(out_folder + "/P2.csv")
    q1 = pd.read_csv(out_folder + "/Q1.csv")
    q2 = pd.read_csv(out_folder + "/Q2.csv")

    layout = go.Layout(
        legend=dict(x=0.9, y=0.9),
        xaxis=dict(
            title="z",
            exponentformat='power',
            showticksuffix='all',
            showtickprefix='all',
            showexponent='all',
            # autotick=True,
            # type='log',
            nticks=5,
            tickfont=dict(
                size=16
            ),
            # autorange='reversed'
        ),
        yaxis=dict(
            title="Angle deviation from linear in degrees",
            # tickformat='.1e',
            exponentformat='power',
            ticks='',
            # tick0=0,
            # dtick=1,
            # tickangle=-45,
            # type='log',
            tickfont=dict(
                size=16
            ),
            range=[0, 3],

        ),
        font=dict(
            size=24
        ),
        hovermode='closest'
    )

    data = []
    data.extend(plot(p1, "P1"))
    data.extend(plot(p2, "P2"))
    data.extend(plot(q1, "Q1"))
    data.extend(plot(q2, "Q2"))



    # data.extend(plot(hs, ratio, "Spline"))


    fig = go.Figure(data=data, layout=layout)
    if output is not None:
        plotly.plot(fig, image="svg", image_filename=output)
    else:
        plotly.plot(fig)
