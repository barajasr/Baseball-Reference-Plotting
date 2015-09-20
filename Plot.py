import os
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np

import Auxiliary as aux
import BrefScraper as brf

class Plot(object):
    """ With data obtained from BrefScraper, Plot clean the raw
        data and saves it to file.
    """
    def __init__(self, scraper=brf.BrefScraper(), histogram=True):
        """ Set defaults to be used later in cleaning and plotting
        """
        self.scraper = scraper
        self.histogram = histogram

        # Axes limit hints to use
        self.x_min = 1
        self.x_max = 10
        self.y_min = -24
        self.y_max = 24

        # Constants
        self.major, self.minor = 6, 3

    def _clean_data(self, data):
        """ For given raw data, split it and fill in missing keys
            with zeroes.
        """
        x_max = self._max_key(data)
        negative, positive = [], []
        bi_keys = aux.LOSS, aux.WIN

        for index in range(self.x_min, x_max+1):
            negative.append(0)
            positive.append(0)
            if index in data[bi_keys[0]]:
                negative[-1] = -data[bi_keys[0]][index]
                if not self.histogram:
                    if index != 0 or self.x_min != 0:
                        negative[-1] *= index

            if index in data[bi_keys[1]]:
                positive[-1] = data[bi_keys[1]][index]
                if not self.histogram:
                    if index != 0 or self.x_min != 0:
                        positive[-1] *= index

        return aux.Data(negative, positive)

    def _fit_y_axis(self, data):
        """ Adjust Y-axis range to next minor tick if required.
        """
        y_min, y_max = self.y_min, self.y_max
        set_min = min(data.negative)
        if set_min <= self.y_min:
            y_min = set_min - (self.minor - set_min % self.minor)
        set_max = max(data.positive)
        if set_max >= self.y_max:
            y_max = set_max + (self.minor - set_max % self.minor)
        return aux.Axis(y_min, y_max)

    def _max_key(self, data):
        """ Return the max x-axis value found in keys.
        """
        dict_max = max([key for sub_data in data.values()
                        for key in sub_data])
        key_max = self.x_max
        if dict_max > self.x_max:
            key_max = dict_max
        return key_max

    def plot(self, plot_type, average):
        """ Main point of entry. Set off scraper, process and plot data.
        """
        # Dict with appropiate functions for data transforming defined
        # at bottom of module.
        (self.x_min, teams_raw, team_set, get_clean, to_plot) = OPTIONS[plot_type]
        cumulative = aux.Data([], [])
        for team, raw_data in teams_raw(self.scraper):
            raw_set = team_set(raw_data)
            data = get_clean(self, raw_set)
            to_plot(self, team, data)

            if average:
                aux.aggragate_cumulative(cumulative, data)

        if average:
            aux.average_data(cumulative, len(self.scraper.teams))
            to_plot(self, 'League Average', cumulative)

    def _plot_outcome_conceding(self, team, data):
        """ Sets the specific params for of win/loss outcome when team concedes
            x runs.
        """
        y_axis = self._fit_y_axis(data)
        record = aux.outcome_record(data, self.histogram)

        y_label = 'Wins/losses when conceding x runs' if self.histogram else\
                  'Total runs sorted by runs conceded per game'
        tag_label = 'outcome_conceding_histogram' if self.histogram else\
                    'outcome_conceding_sorted'

        self._plot_team(data,
                        record,
                        aux.Labels(team, 'Runs conceded', y_label, tag_label),
                        y_axis)

    def _plot_outcome_scoring(self, team, data):
        """ Sets the specific params for of win/loss outcome when team scores
            x runs.
        """
        y_axis = self._fit_y_axis(data)
        record = aux.outcome_record(data, self.histogram)

        y_label = 'Wins/losses when scoring x runs' if self.histogram else\
                  'Total runs sorted by runs scored per game'
        tag_label = 'outcome_scoring_histogram' if self.histogram else\
                    'outcome_scoring_sorted'

        self._plot_team(data,
                        record,
                        aux.Labels(team, 'Runs scored', y_label, tag_label),
                        y_axis)

    def _plot_team(self, data, record, labels, y_axis):
        """ Generic plotting for data found on the team's schedule and results
            page.
        """
        net = [n + m for m, n in zip(data.negative, data.positive)]

        fig = plt.figure()
        plt.xlabel(labels.x)
        plt.ylabel(labels.y)
        # record turned into string for int/float possibilty
        if isinstance(record.wins, int):
            plt.title('{} ({}-{}) - {}'\
               .format(labels.team, record.wins, record.losses, self.scraper.year))
        else:
            plt.title('{} ({:.2f}-{:.2f}) - {}'\
               .format(labels.team, record.wins, record.losses, self.scraper.year))

        x_max = len(data.negative) + 1 if self.x_min == 1 else len(data.negative)
        plt.axis([self.x_min, x_max, y_axis.min, y_axis.max])
        ax = plt.subplot()
        ax.set_xticks(np.arange(1, x_max, 1))
        major_locator = ticker.MultipleLocator(self.major)
        major_formatter = ticker.FormatStrFormatter('%d')
        minor_locator = ticker.MultipleLocator(self.minor)
        ax.yaxis.set_major_locator(major_locator)
        ax.yaxis.set_major_formatter(major_formatter)
        ax.yaxis.set_minor_locator(minor_locator)

        x_axis = range(self.x_min, x_max)
        ax.bar(x_axis, data.negative, width=0.96, color='r', edgecolor=None, linewidth=0)
        ax.bar(x_axis, data.positive, width=0.96, color='b', edgecolor=None, linewidth=0)
        ax.bar(x_axis, net, width=0.96, color='g', edgecolor=None, linewidth=0, label='Net')
        plt.axhline(0, color='black')

        plt.grid(which='both')
        ax.grid(which='minor', alpha=0.5)
        ax.grid(which='major', alpha=0.9)

        legend = ax.legend(loc='best')
        frame = legend.get_frame()
        frame.set_facecolor('0.90')

        self._save(labels.team, labels.tag)

    def _plot_win_loss_margins(self, team, data):
        """ Sets the specific params for margins of win/loss plot.
        """
        y_axis = self._fit_y_axis(data)
        wins = sum(data.positive) if self.histogram else\
               sum([runs // (margin + 1) \
               for margin, runs in enumerate(data.positive)])
        losses = -sum(data.negative) if self.histogram else\
                 -sum([runs // (margin + 1) \
                 for margin, runs in enumerate(data.negative)])

        y_label = '# of times won/loss by margin' if self.histogram else\
                  'Total Runs sorted by margin'
        tag_label = 'margin_histogram' if self.histogram else 'margin_sorted'

        self._plot_team(data,
                        aux.Record(wins, losses),
                        aux.Labels(team, 'Margin of win/loss', y_label, tag_label),
                        y_axis)

    def _plot_win_loss_streaks(self, team, data):
        """ Sets the specific params for win/loss streaks plot.
        """
        y_axis = self._fit_y_axis(data)
        wins = sum([(m + 1) * n for m, n in enumerate(data.positive)]) \
               if self.histogram else sum(data.positive)
        losses = -sum([(m + 1) * n for m, n in enumerate(data.negative)]) \
                 if self.histogram else -sum(data.negative)

        y_label = '# of Streaks' if self.histogram else 'Win/Losses sorted by streak'
        tag_label = 'streaks_histogram' if self.histogram else 'streaks_sorted'

        self._plot_team(data,
                        aux.Record(wins, losses),
                        aux.Labels(team, 'Streak Length', y_label, tag_label),
                        y_axis)

    def _save(self, filename, directory, ext='png', close=True, verbose=True):
        """ Save the current plot to file.
        """
        # Unpack list with splat
        year = self.scraper.year
        path = year if directory == [] else os.path.join(year, directory)
        if not os.path.exists(path):
            os.makedirs(path)

        savepath = os.path.join(path, filename + '.' + ext)
        if verbose:
            print("Saving figure to '{}'...".format(savepath))
        plt.savefig(savepath)
        if close:
            plt.close()

    def set_default_axes(self, x_min=1, x_max=10, y_min=-24, y_max=24):
        """ Adjust default axes range.
        """
        self.x_min, self.x_max = x_min, x_max
        self.y_min, self.y_max = y_min, y_max

# Data transformation and plotting chain
OPTIONS = {'outcome_conceding': [0,
                                 brf.BrefScraper.game_scores,
                                 aux.outcome_when_conceding,
                                 Plot._clean_data,
                                 Plot._plot_outcome_conceding],
           'outcome_scoring': [0,
                               brf.BrefScraper.game_scores,
                               aux.outcome_when_scoring,
                               Plot._clean_data,
                               Plot._plot_outcome_scoring],
           'win_loss_streaks' : [1,
                                 brf.BrefScraper.wins_losses,
                                 aux.count_wins_losses,
                                 Plot._clean_data,
                                 Plot._plot_win_loss_streaks],
           'win_loss_margins' : [1,
                                 brf.BrefScraper.game_scores,
                                 aux.win_loss_margins,
                                 Plot._clean_data,
                                 Plot._plot_win_loss_margins]}
