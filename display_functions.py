import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from utililty import *
from data_functions import  data_prep
import numpy as np

def app_layout_init():
    dates = get_experiment_dates(animal,main_folder)
    min_date,max_date = dt.strptime(dates[0], '%Y%m%d'),dt.strptime(dates[-1], '%Y%m%d')

    component =  html.Div([
        html.H1("Animal Performance"),
        html.Div(["Animal ID: " + animal],id="animal_id"),
        html.Div(['Select Date:',
        dcc.DatePickerSingle(
            id='date-picker-single',
            date=max_date,
            min_date_allowed=min_date,
            max_date_allowed=max_date,
            className= "date_input_1"
        )],className="date_select"),
        html.Hr(),
        html.Div(children = [
            "Trials Attempted By Hour",
            dcc.Graph(id='trial-activity')
        ],className= "plot left"),

        html.Div(children=[
            "Performance Stats For Selected Day",
            dcc.Graph(id='hourly-stats-plot')
        ], className="plot right"),

        html.Div(children=[
            "Performance Stats All-time",
            dcc.Graph(id='daily-stats-plot')
        ], className="plot-full left"),

    ], id ='body') # id body

    data_prep(animal,dates) # prepare data for display

    return component

def generate_trials_figure(stats,desired_date,av_stats,stats_cd):

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
                    x=stats_cd[action]['t'],
                    y=stats_cd[action]['prob_t'],
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

    figure_trials = {
        'data': plot_trials,
        'layout': dict(
            # title={
            #     'text': "Trials Attempted By Hour",
            #     'y': 0.9,
            #     'x': 0.5,
            #     'xanchor': 'center',
            #     'yanchor': 'top',
            #     'font': '19'},
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