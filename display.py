import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from datetime import datetime as dt
from data_processing import *
import os, os.path
import numpy as np



def generate_trials_figure(stats,desired_date,av_stats):

    plot_trials = []
    plot_stats = []
    plot_stats_daily = []
    hours = np.arange(1,25)

    plot_trials.append(
        go.Bar(
            x=hours,
            y=stats['trials'],
            name=desired_date,
        )
    )

    plot_trials.append(
        go.Bar(
            x=hours,
            y=av_stats['trials'],
            error_y=dict(type='data', array=av_stats['std']),
            name='Mean activity',
        )
    )

    for action in stats.keys():
        if action != 'trials':
            plot_stats.append(
                go.Scatter(
                    x=stats[action]['t'],
                    y=stats[action]['prob_t'],
                    mode='lines',
                    name=action
                )
            )

    for action in stats.keys():
        if action != 'trials':
            plot_stats_daily.append(
                go.Scatter(
                    x=np.arange(len(av_stats[action])),
                    y=av_stats[action],
                    mode='lines',
                    name=action
                )
            )

    # plot.append(
    #     go.Scatter(
    #         x=stats['Hit 1']['t'],
    #         y=stats['Hit 1']['prob_t'],
    #         mode='lines+markers',
    #         name='Hit 1'
    #     )
    # )

    figure_trials = {
        'data': plot_trials,
        'layout': dict(
            xaxis={'title': 'Time of Day',
                   'range': [0, 24],
                   'tickmode': 'linear',
                   'tick0': 0,
                   'dtick':1},
            yaxis={'title': 'Number of trials'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest',
            showlegend=True,
            legend=go.layout.Legend(
                x=0,
                y=1.0
            )
        )
    }

    figure_stats = {
        'data': plot_stats,
        'layout': dict(
            xaxis={'title': 'Time of Day',
                   'range': [0, 24],
                   'tickmode': 'linear',
                   'tick0': 0},
            yaxis={'title': 'Probability'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest',
            showlegend=True,
            legend=go.layout.Legend(
                x=0,
                y=1.0
            )
        )
    }

    figure_stats_daily = {
        'data': plot_stats_daily,
        'layout': dict(
            xaxis={'title': 'Day',
                   'tickmode': 'linear',
                   'tick0': 0},
            yaxis={'title': 'Probability'},
            margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            hovermode='closest',
            showlegend=True,
            legend=go.layout.Legend(
                x=0,
                y=1.0
            )
        )
    }

    return [figure_trials,figure_stats,figure_stats_daily]