import urllib3
import bs4

from collections import namedtuple

AL = ['BAL', 'BOS', 'CHW', 'CLE', 'DET', 'HOU', 'KCR',
      'LAA', 'MIN', 'NYY', 'OAK', 'SEA', 'TBR', 'TEX', 'TOR']
NL = ['ARI', 'ATL', 'CHC', 'CIN', 'COL', 'LAD', 'MIA',
      'MIL', 'NYM', 'PHI', 'PIT', 'SDP', 'SFG', 'STL', 'WSN']
MLB = sorted(AL + NL)
Content = namedtuple('Content', 'team data')

class BrefScraper(object):
    """ Class used for scrapping baseball reference team pages.
    """
    def __init__(self, teams=MLB, year='2015', playoffs=False):
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
            # Contents in [u'...'] form
            result.append([cast(tds[column].contents[0]) for column in columns])
        return result

    def _get_rows(self, team):
        """ Return all table rows requested; including playoffs is flag set.
        """
        url = 'http://www.baseball-reference.com/teams/{}/{}'\
              '-schedule-scores.shtml'.format(team, self.year)

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
        for team in self.teams:
            runs = self._get_columns(self._get_rows(team), [8, 9], int)
            yield Content(team, runs)

    def wins_losses(self):
        """ Yield a list with (team, ['W', 'L',...]) win/loss occurances.
        """
        for team in self.teams:
            # win_loss in [u'[L|T|W](-wo)?'] form
            outcomes = [win_loss[0][0] for win_loss in
                        self._get_columns(self._get_rows(team), [7])]
            yield Content(team, outcomes)
