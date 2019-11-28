import os
from os.path import isdir,join
import datetime
from datetime import datetime as dt
import multiprocessing as mp
import dash_core_components as dcc
import dash_html_components as html
from mouse_activity_stats import get_performance_stats, get_trial_activity
import linecache

animal = 'test5_2AFC'
main_folder = "LabVIEW Data"
mouse_actions = ['Hit 1', 'Hit 2', 'FA 1', 'FA 2', 'Miss 1', 'Miss 2']


def get_experiment_dates(animal,main_folder):
    folders = [f for f in os.listdir(main_folder) if isdir(join(main_folder, f)) if animal in f]
    dates = [folder.split("_")[-1] for folder in folders]
    dates.sort()

    return dates

def convert_time_to_float(time):
    # convert a time to a float, i.e 06:30:00 => 6.5, for plotting
    h,m,s = time.split(':')
    h,m,s = float(h),float(m),float(s)
    return np.round(h + m/60 + s/3600,3)

def write_data_to_file(date_stats,total_count,date):
    stats_dir = join('stats',date)
    mouse_actions = date_stats.keys()

    for mouse_action in mouse_actions:
        if mouse_action != "trials":
            stats_file_path = join(stats_dir, mouse_action + ".txt")
            stats_file = open(stats_file_path, "w+")
            current_action_stats = date_stats[mouse_action]
            count, prob_t, t = current_action_stats['count'], current_action_stats['prob_t'], current_action_stats['t']
            stats_file.write(str(total_count) + '\t' + str(count))
            stats_file.write('\n')

            for i in range(len(prob_t)):
                stats_file.write(str(prob_t[i]) + '\t' + str(t[i]))
                stats_file.write('\n')
            stats_file.close()


def get_stats(animal,date,main_folder = 'LabVIEW Data',toReturn='11'):
    # gets the number of trials perfomred at each hour, and the performance stats for a given date,
    # specified by the name of the folder with format animalname_date

    folder = animal + "_" + date
    lab_view_output_file = join(main_folder,folder, "%s%s.txt" % (animal, date))

    time, trialCount, events = np.loadtxt(lab_view_output_file, dtype='str', delimiter='\t', usecols=(1, 2, 3),unpack=True)  # Read in \t separated data
    time = np.array([convert_time_to_float(t_stamp[:8]) for t_stamp in time[1:]]) # keep only the hour and ignore first row since it contains titles

    if toReturn == '11':
        trial_dist = get_trial_activity(trialCount, time)
        performance_stats,_ = get_performance_stats(events, time, date)
        current_date_stats = {**performance_stats, **trial_dist}
        return current_date_stats
    if toReturn[0] == '1':
        trial_dist = get_trial_activity(trialCount,time)
        current_date_stats = {**trial_dist}
        return current_date_stats
    if toReturn[-1] == '1':
        performance_stats,total_count = get_performance_stats(events,time,date)
        current_date_stats = {**performance_stats}
        return current_date_stats,total_count

def data_prep(animal,dates,stats_dir = "stats"):
    for date in dates:
        date_stats_dir = join(stats_dir,date)
        pool = mp.Pool(mp.cpu_count())

        if isdir(date_stats_dir) == 0:
            os.mkdir(stats_dir)
            toReturn = '01'
            date_stats,total_count = pool.apply(get_stats, args=(animal, date, toReturn))
            pool.apply(write_data_to_file,args=(date_stats,total_count,date))

        pool.close()

def get_prior_stats(date):
    stats_dir = join('stats',date)

    date_dt = dt.strptime(date, '%Y%m%d')
    prev_date_dt = date_dt - datetime.timedelta(1)

    prev_date = str(prev_date_dt.year) + str(prev_date_dt.month) + str(prev_date_dt.day)
    exp_dates = get_experiment_dates(animal,main_folder)

    count = dict.fromkeys(mouse_actions)
    count['total'] = 0

    if prev_date in exp_dates:
        for mouse_action in mouse_actions:
            stats_file = join(stats_dir,mouse_action + ".txt")
            total_count, action_count = linecache.getline(stats_file,0).split("\t")
            count['total'] = total_count
            count[mouse_action] = action_count

    return count


def app_layout_init():
    dates = get_experiment_dates(animal,main_folder)
    min_date,max_date = dt.strptime(dates[0], '%Y%m%d'),dt.strptime(dates[-1], '%Y%m%d')

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

    data_prep(animal,dates) # prepare data for display

    return component