import numpy as np


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