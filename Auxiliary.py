from collections import namedtuple

RK = 0          # Ignore, relevant for online sorting
GM = 1          # Game number of the season
DATE = 2        # Date of game
BOX = 3         # Link to boxscore
TM = 4          # Team looking up
HOME_AWAY = 5   # '' = home, '@' = away
OPP = 6         # Opponent
WIN_LOSS = 7    # Win, loss, walkoff; '[W|L](-wo)?'
RF = 8          # Runs scored
RA = 9          # Runs scored against
INN = 10        # Innings played if extras, '' otherwise
RECORD = 11     # Running win/loss record
RANK = 12       # Rank within division
GB = 13         # Games back '[  Tied|(up )?\d.\d]'
WIN_P = 14      # Winning pitcher
LOSS_P = 15     # Lossing pitcher
SAVE_P = 16     # Saving pitcher if any
TIME = 17       # Duration of game
DAY_NIGHT = 18  # Day/Night game
ATTD = 19       # Number of attendees
STREAK = 20     # Win/loss streak; '[-|+]+'

TARGETS = ['scores', 'wins_losses']
LOSS, WIN = 'L', 'W'

Axis = namedtuple('Axis', 'min max')
Data = namedtuple('Data', 'negative positive')
Labels = namedtuple('Labels', 'team x y tag')
Record = namedtuple('Record', 'wins, losses')

def aggragate_cumulative(cumulative, to_add):
    """ Increment/insert values from new set into the cumulative set.
    """
    for index in range(len(to_add.negative)):
        if index < len(cumulative.negative):
            cumulative.negative[index] += to_add.negative[index]
            cumulative.positive[index] += to_add.positive[index]
        else:
            cumulative.negative.append(to_add.negative[index])
            cumulative.positive.append(to_add.positive[index])

def average_data(cumulative, number_of_teams):
    """ Given the whole set, average for number of teams.
    """
    for index in range(len(cumulative.negative)):
        cumulative.negative[index] /= number_of_teams
        cumulative.positive[index] /= number_of_teams

def columns_values(tds):
    """ Take in the list of table data cells and return the values required.
    """
    similar = [RK, GM, TM, HOME_AWAY, OPP, WIN_LOSS, RF, RA, INN,
               RECORD, RANK, GB, TIME, DAY_NIGHT, ATTD, STREAK]
    for index in similar:
        tds[index] = tds[index].text

    similar = [WIN_P, LOSS_P, SAVE_P]
    for index in similar:
        tds[index] = '' if tds[index].text == '' else\
                     tds[index].find('a').get('title')

    # Playoffs changes behavior
    has_link = tds[DATE].find('a')
    if has_link is not None:
        tds[DATE] = has_link.text
    else:
        tds[DATE] = tds[DATE].text

    # Early 1900s may not have boxscores
    has_link = tds[BOX].find('a')
    if has_link is not None:
        tds[BOX] = has_link.text
    else:
        tds[BOX] = tds[BOX].text

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

