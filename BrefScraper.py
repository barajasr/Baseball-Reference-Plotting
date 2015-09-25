import bs4
import csv
import os
import urllib3

from collections import namedtuple

import Auxiliary as aux

AL = ['BAL', 'BOS', 'CHW', 'CLE', 'DET', 'HOU', 'KCR',
      'LAA', 'MIN', 'NYY', 'OAK', 'SEA', 'TBR', 'TEX', 'TOR']
NL = ['ARI', 'ATL', 'CHC', 'CIN', 'COL', 'LAD', 'MIA',
      'MIL', 'NYM', 'PHI', 'PIT', 'SDP', 'SFG', 'STL', 'WSN']
MLB = sorted(AL + NL)
Content = namedtuple('Content', 'team data')

class BrefScraper(object):
    """ Class used for scrapping baseball reference team pages.
    """
    def __init__(self, teams=MLB, year='2015', playoffs=False, from_csv=False):
        """ Prep class for scrapping for information.
        """
        def valid_teams_subset(teams):
            """ Ensure teams list is valid.
            """
            for team in teams:
                if team not in MLB:
                    return False
            return True
        if not valid_teams_subset(teams):
            raise ValueError('{} contains one or more invalid entries.'
                             .format(teams))
        self.year = year
        self.teams = teams
        self.playoffs = playoffs
        self.from_csv = from_csv

        self.base_url = 'http://www.baseball-reference.com/'
        self.team_post = '-schedule-scores.shtml'

        self.csv = 'CSV'
        self.delimiter = ';'

    def _get_all_columns(self, rows):
        """ Yield all columns of table row. Used for writing to file.
        """
        for row in rows:
            tds = row.findAll('td')
            if len(tds) < 21:
                continue
            if tds[0].contents == [] and not self.playoffs:
                break
            aux.columns_values(tds)
            yield tds

    def _get_columns(self, rows, columns, cast=str):
        """ Yield filtered column(s) from table rows until exhausted.
            Results from playoffs included if flag was set.
        """
        result = []
        for row in rows:
            tds = row.findAll('td')
            # Skip unfinished games, table row headers,and possibly playoffs
            if len(tds) < 21:
                continue
            if tds[0].contents == [] and not self.playoffs:
                break
            result.append([cast(tds[column].text) for column in columns])
        return result

    def _get_rows(self, team):
        """ Return all table rows requested; including playoffs is flag set.
        """
        url = '{}/teams/{}/{}{}'.format(self.base_url,
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
            Results from playoffs included if flag is set.
        """
        cast = int
        for team in self.teams:
            runs = []
            if not self.from_csv:
                runs = self._get_columns(self._get_rows(team),
                                         [aux.RF, aux.RA],
                                         cast)
            else:
                runs = [[cast(row[aux.RF]), cast(row[aux.RA])] \
                       for row in self._read_from_file(team)]
            yield Content(team, runs)

    def _read_from_file(self, team):
        """ Yield all rows for each team requested. Fails if any team is not
            found.
        """
        # 162 Seasonal games (strike/shortened years exception)
        filepath = os.path.join(self.year, self.csv, '{}.csv'.format(team))
        if not os.path.exists(filepath):
            raise Exception('Error: {} does not exists.'.format(filepath))

        end = 162 if not self.playoffs else None
        with open(filepath, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile, delimiter=self.delimiter)
            return [row for row in reader][:end]

    def save_to_file(self):
        """ Write all data for teams requested to file for archiving.
        """
        path = os.path.join(self.year, self.csv)
        if not os.path.isdir(path):
            os.makedirs(path)

        for team in self.teams:
            filepath = os.path.join(path, '{}.csv'.format(team))
            with open(filepath, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, delimiter=self.delimiter)
                for entry in self._get_all_columns(self._get_rows(team)):
                    writer.writerow(entry)

    def wins_losses(self):
        """ Yield a list with (team, ['W', 'L',...]) win/loss occurances.
        """
        for team in self.teams:
            outcomes = []
            if not self.from_csv:
                # win_loss in [u'[L|T|W](-wo)?'] form
                outcomes = [win_loss[0][0] for win_loss in
                            self._get_columns(self._get_rows(team),
                                              [aux.WIN_LOSS])]
            else:
                outcomes = [row[aux.WIN_LOSS][0] \
                       for row in self._read_from_file(team)]
            yield Content(team, outcomes)
