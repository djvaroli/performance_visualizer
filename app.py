import dash
from display import *
from utils import *
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

animal = 'test5_2AFC'
main_folder = "LabVIEW Data"

def app_layout_init():
    dates = get_experiment_dates(animal,main_folder)
    min_date,max_date = dt.strptime(dates[0], '%Y%m%d'),dt.strptime(dates[-1], '%Y%m%d')

    # dcc.Slider(
    #     min=0,
    #     max=len(dates),
    #     marks={i: ' {}'.format(i) for i in range(10)},
    #     value=5,
    # )

    component =  html.Div([
        html.H1('Mouse Activity'),
        html.Label('Select Date:'),
        dcc.DatePickerSingle(
            id='date-picker-single',
            date=max_date,
            min_date_allowed=min_date,
            max_date_allowed=max_date
        ),
        dcc.Graph(id='trial-activity'),
        dcc.Graph(className='behavior-stats-plot', id='hourly-stats-plot'),
        dcc.Graph(className='behavior-stats-plot', id='daily-stats-plot')
    ], id ='body') # id body

    return component

app.layout = app_layout_init

@app.callback(
    [Output('trial-activity', 'figure'), Output('hourly-stats-plot','figure'),Output('daily-stats-plot','figure')],
    [Input('date-picker-single','date')])
def update_trials_figure(selected_date):

    dates = get_experiment_dates(animal,main_folder)
    selected_date = selected_date.replace('-','')[:8]
    stats = get_stats(animal,selected_date)

    av_stats = dict.fromkeys(stats.keys())
    for key in av_stats.keys():
        av_stats[key] = []

    for date in dates:
        stats_for_date = get_stats(animal,date)

        for key in av_stats.keys():
            if key != 'trials':
                av_stats[key] += [stats_for_date[key]['prob_t'][-1]]
        else:
            av_stats['trials'] += [stats_for_date['trials']]

    av_stats['std'] = np.std(av_stats['trials'],axis=0)
    av_stats['trials'] = np.average(av_stats['trials'],axis=0)

    return generate_trials_figure(stats,selected_date,av_stats)

if __name__ == '__main__':
    app.run_server(debug=True)


## if the file with data exists, load it, if not compute the probs and save it to file 