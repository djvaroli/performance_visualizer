import os, os.path
import numpy as np
import pdb


def get_performance_stats(events, time, date, mouse_actions = None):
    # def load_stats(filepath):
    #     stats_text = np.loadtxt(filepath, dtype='str', delimiter='\t', unpack=True)  # Read in \t separated data
    #     stats = None
    #     return stats

    if mouse_actions is None:
        mouse_actions = ['Hit 1', 'Hit 2', 'FA 1', 'FA 2', 'Miss 1', 'Miss 2']

    stats_dir = os.path.join("stats",date)
    # each mouse action is a key, for each key --> dictionary with count of that action, probability of that action
    # over time and time points for plotting
    action_stats = dict.fromkeys(mouse_actions)
    for mouse_action in mouse_actions:
        action_stats[mouse_action] = {'count': 0, 'prob_t': [], 't': []}

    # if os.path.isdir(stats_dir):
    #     for mouse_action in mouse_actions:
    #         stats_file_path = os.path.join(stats_dir,mouse_action + ".txt")
    #         stats_data = load_stats(stats_file_path)
    #         action_stats[mouse_action]['count'] = stats_data[0]
    #         action_stats[mouse_action]['prob_t'] = stats_data[1]
    #         action_stats[mouse_action]['t'] = stats_data[2]
    #     return action_stats

    if os.path.isdir(stats_dir) == 0:
        os.mkdir(stats_dir)

    total_count = 0
    for i in range(len(events)):
        event = events[i]
        for mouse_action in mouse_actions:
            if mouse_action in event:
                total_count += 1
                action_stats[mouse_action]['count'] += 1
                prob = action_stats[mouse_action]['count']/total_count
                action_stats[mouse_action]['prob_t'] += [np.round(prob,3)]
                action_stats[mouse_action]['t'] += [time[i]]


    # for mouse_action in mouse_actions:
    #     stats_file_path = os.path.join(stats_dir, mouse_action + ".txt")
    #     stats_file = open(stats_file_path, "w+")
    #     current_action_stats = action_stats[mouse_action]
    #     count,prob_t,t = current_action_stats['count'],current_action_stats['prob_t'],current_action_stats['t']
    #     stats_file.write(mouse_action + '\t' + str(count))
    #     stats_file.write('\n')
    #     for i in range(len(prob_t)):
    #         stats_file.write(str(prob_t[i]) + '\t' + str(t[i]))
    #         stats_file.write('\n')
    #     stats_file.close()

    return action_stats
