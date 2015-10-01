import bs4
import csv
import os
import urllib3

from collections import namedtuple

import Auxiliary as aux
import Teams

CSV = ['', 'r', 'w']
Content = namedtuple('Content', 'team data')

class BrefScraper(object):
    """ Class used for scrapping baseball reference team pages.
    """
    def __init__(self, teams=Teams.MLB, year='2015', playoffs=False, csv_mode=''):
        """ Prep class for scrapping for information.
        """
        if teams in Teams.LEAGUES:
            teams = Teams.TEAMS[teams](year)
        else:
            if not Teams.valid_teams_subset(year, teams):
                raise ValueError('{} contains one or more invalid entries.'
                                 .format(teams))
        self.year = year
        self.teams = teams
        self.playoffs = playoffs

        self.base_url = 'http://www.baseball-reference.com/'
        self.team_post = '-schedule-scores.shtml'

        self.csv = 'CSV'
        if csv_mode not in CSV:
            raise ValueError('{} is not found in {}.'
                             .format(csv_mode, CSV))
        self.csv_mode = csv_mode
        self.delimiter = ';'

    def _get_columns(self, rows, columns, cast=str):
        """ Return filtered column(s) from table rows.
        """
        result = []
        for row in rows:
            result.append([cast(row[column]) for column in columns])
        return result

    def _get_rows(self, team):
        """ Return all table rows requested.
        """
        url = '{}teams/{}/{}{}'.format(self.base_url,
                                        team,
                                        self.year,
                                        self.team_post)

        http = urllib3.PoolManager()
        with http.request('GET', url) as resp:
            # resp is in bytes
            soup = bs4.BeautifulSoup(resp.data.decode())
            return soup.find('table', id='team_schedule')\
                       .find('tbody')\
                       .findAll('tr')

    def game_scores(self):
        """ Yields a list of (team, [[RF, RA], ...]) for games found in table
            rows.
        """
        for team in self.teams:
            data = self._process_team(team)
            yield Content(team,
                          self._get_columns(data, [aux.RF, aux.RA], int))

    def _parse_rows(self, rows):
        """ Return all columns of table row in proper format to be used later.
            Data from playoffs included if flag is set.
        """
        result = []
        for row in rows:
            tds = row.findAll('td')
            if len(tds) < 21:
                continue
            if tds[0].contents == [] and not self.playoffs:
                break
            aux.columns_values(tds)
            result.append(tds)

        return result

    def _process_team(self, team):
        """ For team, get corresponding table data, and prep data for usage.
            If applicable read from file or download and/or save to file.
        """
        data = []
        if self.csv_mode != 'r':
            data = self._parse_rows(self._get_rows(team))
            if self.csv_mode == 'w':
                self._save_to_file(team, data)
        else:
            data = self._read_from_file(team)

        return data

    def _read_from_file(self, team):
        """ Return all rows for each team requested. Fails if any team is not
            found.
        """
        filepath = os.path.join(self.year, self.csv, '{}.csv'.format(team))
        if not os.path.exists(filepath):
            raise Exception('Error: {} does not exists.'.format(filepath))

        # 162 Seasonal games (strike/shortened years exception)
        end = 162 if not self.playoffs else None
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            return [row for row in reader][:end]

    def save_to_file(self):
        """ Write all data for teams requested to file for archiving.
        """
        for team in self.teams:
            # Ignore returned data, saves with flag set
            self._process_team(team)

    def _save_to_file(self, team, rows):
        """ Write all data for specified team to file for archiving.
        """
        path = os.path.join(self.year, self.csv)
        if not os.path.isdir(path):
            os.makedirs(path)

        filepath = os.path.join(path, '{}.csv'.format(team))
        print("Saving team data to '{}'...".format(filepath))
        with open(filepath, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=self.delimiter)
            for entry in rows:
                writer.writerow(entry)

    def wins_losses(self):
        """ Yield a list with (team, ['W', 'L',...]) win/loss occurances.
        """
        for team in self.teams:
            data = self._process_team(team)
            # win_loss in [u'[L|T|W](-wo)?'] form
            yield Content(team,
                          [win_loss[0][0] for win_loss in \
                          self._get_columns(data, [aux.WIN_LOSS])])

