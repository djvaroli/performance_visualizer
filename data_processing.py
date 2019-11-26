import os, os.path
import numpy as np
from get_performance_stats import *
from get_trial_activity import *
import pdb

def get_stats(animal,date,main_folder = 'LabVIEW Data', ext = ".txt"):
    # gets the number of trials perfomred at each hour, and the performance stats for a given date,
    # specified by the name of the folder with format animalname_date
    def convert_time_to_float(time):
        # convert a time to a float, i.e 06:30:00 => 6.5, for plotting
        h,m,s = time.split(':')
        h,m,s = float(h),float(m),float(s)
        return np.round(h + m/60 + s/3600,3)

    # get all folders for the current animal
    folder = animal + "_" + date
    date = folder.split("_")[-1]
    lab_view_output_file = os.path.join(main_folder,folder, "%s%s.txt" % (animal, date))

    time, trialCount, events = np.loadtxt(lab_view_output_file, dtype='str', delimiter='\t', usecols=(1, 2, 3),unpack=True)  # Read in \t separated data
    time = np.array([convert_time_to_float(t_stamp[:8]) for t_stamp in time[1:]]) # keep only the hour and ignore first row since it contains titles

    trial_dist = get_trial_activity(trialCount,time)
    performance_stats = get_performance_stats(events,time,date)
    current_date_stats = {**trial_dist, **performance_stats}

    return current_date_stats


def get_cumulative_stats(main_folder,folders, animal):
    dates = [f.split("_")[-1] for f in folders].sort()
    cumulative_stats = dict.fromkeys(dates)

    if os.path.isdir("stats") == False:
        os.mkdir("stats")


    all_stats = np.zeros((len(folders), 24))
    for ifolder in range(len(folders)):
        folder = folders[ifolder]
        folder_path = os.path.join(main_folder, folder)
        stats = get_stats(animal, folder_path)
        all_stats[ifolder] = stats

    return all_stats



# def convert_time_to_float(time):
#     # convert a time to a float, i.e 06:30:00 => 6.5
#     h,m,s = time.split(':')
#     h,m,s = float(h),float(m),float(s)
#     return np.round(h + m/60 + s/3600,3)
#
# datafile = "/Users/danielvaroli/Desktop/jerry_chen_lab/acitivty_visualizer/LabVIEW Data/test4_2AFC_20191112/test4_2AFC20191112.txt"
# time, trialCount, events = np.loadtxt(datafile, dtype='str', delimiter='\t', usecols=(1, 2, 3),
#                                       unpack=True)
#
# events = events[1:]
# time = np.array([convert_time_to_float(t_stamp[:8]) for t_stamp in
#                  time[1:]])
# mouse_actions = ['Hit 1', 'Hit 2', 'FA 1', 'FA 2', 'Miss 1', 'Miss 2']
#
# # calculate_performance_stats_for_date(mouse_actions,events,time,"10112019")
# folder = "/Users/danielvaroli/Desktop/jerry_chen_lab/acitivty_visualizer/LabVIEW Data/test4_2AFC_20191112"
# animal = "test4_2AFC"
#
# get_stats(animal,folder)