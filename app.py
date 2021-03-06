import dash
from display_functions import *
from data_functions import *
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = app_layout_init


@app.callback(
    [Output('trial-activity', 'figure'), Output('hourly-stats-plot','figure'),Output('daily-stats-plot','figure')],
    [Input('date-picker-single','date')])
def update_trials_figure(selected_date):

    dates = get_experiment_dates(animal,main_folder)
    selected_date = selected_date.replace('-','')[:8]
    stats, stats_cd = get_stats(animal,selected_date)

    av_stats = dict.fromkeys(stats.keys())
    for key in av_stats.keys():
        av_stats[key] = []

    for date in dates:
        stats_for_date, _ = get_stats(animal,date)
        # print(stats_for_date.keys())
        # print(date)
        for key in av_stats.keys():
            if key != 'trials':
                try:
                    av_stats[key] += [stats_for_date[key]['prob_t'][-1]]
                except:
                    print("Date not yet available.")
        else:
            av_stats['trials'] += [stats_for_date['trials']]

    av_stats['std'] = np.std(av_stats['trials'],axis=0)
    av_stats['trials'] = np.average(av_stats['trials'],axis=0)

    return generate_trials_figure(stats,selected_date,av_stats,stats_cd)

if __name__ == '__main__':
    app.run_server(debug=True)


## if the file with data exists, load it, if not compute the probs and save it to file 