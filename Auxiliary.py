from collections import namedtuple

TARGETS = ['scores', 'wins_losses']
LOSS, WIN = 'L', 'W'

Axis = namedtuple('Axis', 'min max')
Data = namedtuple('Data', 'negative positive')
Labels = namedtuple('Labels', 'team x y tag')
Record = namedtuple('Record', 'wins, losses')

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

def outcome_record(data, histogram):
    """ Return win/loss record of team when using outcome_[conceding|scoring]
        plots. The zero index adds quirk not found in others.
    """
    losses, wins = 0, 0
    if histogram:
        return Record(sum(data.positive),  -sum(data.negative))
    else:
        for index in range(len(data[0])):
            if index > 0:
                wins += data.positive[index] // index
                losses += -data.negative[index] // index
            else:
                wins += data.positive[index]
                losses += -data.negative[index]

    return Record(wins, losses)

def outcome_when_conceding(raw_data):
    """ From incoming list of [[RF, RA], ...] record win/loss wrt RA.
    """
    outcomes_set = {LOSS : {}, WIN : {}}
    for runs_for, runs_against in raw_data:
        outcome = WIN if runs_for - runs_against > 0 else LOSS
        update_dicts(outcomes_set, outcome, runs_against)

    return outcomes_set

def outcome_when_scoring(raw_data):
    """ From incoming list of [[RF, RA], ...] record win/loss relative wrt RF.
    """
    outcomes_set = {LOSS : {}, WIN : {}}
    for runs_for, runs_against in raw_data:
        outcome = WIN if runs_for - runs_against > 0 else LOSS
        update_dicts(outcomes_set, outcome, runs_for)

    return outcomes_set

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

