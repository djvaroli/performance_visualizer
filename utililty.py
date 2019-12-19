import os
import numpy as np
from os.path import isdir,join
import datetime
from datetime import datetime as dt
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


def get_prior_stats(date):
    count = dict.fromkeys(mouse_actions, 0)
    count['total'] = 0

    date_dt = dt.strptime(date, '%Y%m%d')
    prev_date_dt = date_dt - datetime.timedelta(1)
    prev_date = prev_date_dt.strftime('%Y%m%d')
    exp_dates = get_experiment_dates(animal,main_folder)

    if prev_date in exp_dates:
        stats_dir = join('stats', prev_date)
        for mouse_action in mouse_actions:
            stats_file = join(stats_dir,mouse_action + ".txt")
            line = linecache.getline(stats_file,1)
            total_count, action_count = line.replace("\n", "").split("\t")
            total_count = int(total_count)
            action_count = int(action_count)
            count['total'] = total_count
            count[mouse_action] = action_count
    return count


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