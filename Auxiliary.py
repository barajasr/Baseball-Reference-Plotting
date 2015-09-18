""" Authour: Richard Barajas
    Date: Sept. 15, 2015
"""
TARGETS = ['scores', 'wins_losses']
LOSS, WIN = 'L', 'W'

def count_wins_losses(raw_data):
    """ From incoming list of ['W', 'L', ...] record win/loss streaks.
        Return dict with said counts.
    """
    streaks_set, streak, previous = {LOSS:{}, WIN:{}}, 0, ''
    for win_loss in raw_data:
        if previous != '':
            if previous != win_loss:
                update_dicts(streaks_set, previous, streak)
                previous, streak = win_loss, 1
            else:
                streak += 1
        else:
            previous, streak = win_loss, 1

    # Active streak
    update_dicts(streaks_set, previous, streak)
    return streaks_set

def update_dicts(dicts, key, subkey):
    """ Increment or insert subkey relating dict with key as top level dict key.
    """
    if subkey in dicts[key]:
        dicts[key][subkey] += 1
    else:
        dicts[key][subkey] = 1

def win_loss_margins(raw_data):
    """ Return dict recording the occurances of the margin of victory for each
        game; results inserted in either win or loss key provided.
    """
    margins_set = {LOSS : {}, WIN : {}}
    for score in raw_data:
        diff = score[0] - score[1]
        key = WIN
        # First bi_key has to be negative
        if diff < 0:
            key = LOSS
            diff *= -1
        update_dicts(margins_set, key, diff)

    return margins_set

