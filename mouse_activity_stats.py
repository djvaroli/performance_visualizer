from utils import get_prior_stats, mouse_actions
import numpy as np
import pdb

def get_performance_stats(events, time, date):
    # each mouse action is a key, for each key --> dictionary with count of that action, probability of that action
    # over time and time points for plotting
    action_stats = dict.fromkeys(mouse_actions)

    init_count = get_prior_stats(date)

    for mouse_action in mouse_actions:
        count = init_count[mouse_action]
        action_stats[mouse_action] = {'count': count, 'prob_t': [], 't': []}
    total_count = init_count['total']

    for i in range(len(events)):
        event = events[i]
        for mouse_action in mouse_actions:
            if mouse_action in event:
                total_count += 1
                action_stats[mouse_action]['count'] += 1
                prob = action_stats[mouse_action]['count']/total_count
                action_stats[mouse_action]['prob_t'] += [np.round(prob,3)]
                action_stats[mouse_action]['t'] += [time[i]]


    return action_stats,total_count


def adjust_for_resets(trialCount):
    """finds the locations of the varialbe resets, i.e. when trial count goes to 0
        :returns and array of indices of the break-values, i.e. last value before reset
    """

    def detect_resets(trialCount):
        idx_resets = []
        prev_entry = trialCount[0]
        for i in range(1, len(trialCount)):
            new_entry = trialCount[i]
            if prev_entry > new_entry:
                idx_resets += [i - 1]
            prev_entry = new_entry
        return idx_resets

    idx_resets = detect_resets(trialCount)
    new_trial_count = trialCount.copy()

    for i in idx_resets:
        new_trial_count[i:] += trialCount[i]

    return new_trial_count


def get_trial_activity(trialCount,time):
    # computes the number of trials perfomred by the mouse at every hour in the day
    time = np.asarray(time,dtype=int)
    trialCount_int = np.array([int(count) for count in trialCount[1:]]) # convert trials to ints
    trialCount_adjusted = adjust_for_resets(trialCount_int) # resets cause trials to go to 0, rescale everything to cancel that out
    trialCount_cleaned = trialCount_adjusted - trialCount_adjusted[0] # subtract initial number of trials

    hours = np.arange(1, 25)
    n_trials = np.zeros(24)
    # get number of trials at each hour
    for h in hours:
        try:
            times = np.ravel(np.where(time == h))
            start, stop = times[0], times[-1]
        except:
            n_trials[h - 1] = 0
        else:
            n_trials[h - 1] = trialCount_cleaned[stop] - trialCount_cleaned[start]

    trial_dist = {'trials':n_trials}
    return  trial_dist