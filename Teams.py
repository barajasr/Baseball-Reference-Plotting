AL = 'AL'
NL = 'NL'
MLB = 'MLB'
LEAGUES = [AL, NL, MLB]

def mlb_teams(year):
    """ For given year return teams active in the majors.
        Caveat, list is not complete; those included are only those
        with a current team still active.
    """
    year = int(year)
    return sorted(al_teams(year) + nl_teams(year))

def al_teams(year):
    """ For given year return teams existing in AL.
        Caveat, list is not complete; those included are only those
        with a current team still active.
    """
    teams = []
    year = int(year)
    if year >= 1901:
        teams.append('BOS')
        teams.append('CLE')
        teams.append('CHW')
        teams.append('DET')
    else:
        return []
    if year >= 1903:
        teams.append('NYY')
    if year >= 1969:
        teams.append('KCR')
    if year >= 1977:
        teams.append('SEA')
        teams.append('TOR')

    league = AL
    angels(year, teams)
    astros(year, teams, league)
    athletics(year, teams)
    brewers(year, teams, league)
    orioles(year, teams)
    rangers(year, teams)
    rays(year, teams)
    twins(year, teams)
    return sorted(teams)

def nl_teams(year):
    """ For given year return teams existing in NL.
        Caveat, list is not complete; those included are only those
        with a current team still active.
    """
    teams = []
    year = int(year)
    if year >= 1876:
        teams.append('CHC')
    else:
        return []
    if year >= 1883:
        teams.append('PHI')
    if year >= 1887:
        teams.append('PIT')
    if year >= 1890:
        teams.append('CIN')
    if year >= 1892:
        teams.append('STL')
    if year >= 1962:
        teams.append('NYM')
    if year >= 1969:
        teams.append('SDP')
    if year >= 1993:
        teams.append('COL')
    if year >= 1996:
        teams.append('ARI')

    league = NL
    astros(year, teams, league)
    braves(year, teams)
    brewers(year, teams, league)
    dodgers(year, teams)
    giants(year, teams)
    marlins(year, teams)
    nationals(year, teams)
    return sorted(teams)

TEAMS = {AL : al_teams, NL : nl_teams, MLB : mlb_teams}

def angels(year, teams):
    """ Append appropriate Angels abbreviation for year if applicable.
    """
    if year >= 2005:
        teams.append('LAA')
    elif year >= 1997:
        teams.append('ANA')
    elif year >= 1965:
        teams.append('CAL')
    elif year >= 1961:
        teams.append('LAA')

def astros(year, teams, league):
    """ Append appropriate Astros abbreviation for year if applicable.
    """
    if year >= 2013 and league == AL:
        teams.append('HOU')
    elif year >= 1962 and year < 2013  and league == NL:
        teams.append('HOU')

def athletics(year, teams):
    """ Append appropriate Athletics abbreviation for year if applicable.
    """
    if year >= 1968:
        teams.append('OAK')
    elif year >= 1955:
        teams.append('KCA')
    elif year >= 1901:
        teams.append('PHA')

def braves(year, teams):
    """ Append appropriate Braves abbreviation for year if applicable.
    """
    if year >= 1966:
        teams.append('ATL')
    elif year >= 1953:
        teams.append('MLN')
    elif year >= 1876:
        teams.append('BSN')

def brewers(year, teams, league):
    """ Append appropriate Brewers abbreviation for year if applicable.
    """
    if year >= 1970:
        if year >= 1993  and league == NL:
            teams.append('MIL')
        elif year < 1993 and league == AL:
            teams.append('MIL')
    elif year == 1969 and league == AL:
        teams.append('SEP')

def dodgers(year, teams):
    """ Append appropriate Dodgers abbreviation for year if applicable.
    """
    if year >= 1958:
        teams.append('LAD')
    elif year >= 1884:
        teams.append('BRO')

def giants(year, teams):
    """ Append appropriate Giants abbreviation for year if applicable.
    """
    if year >= 1958:
        teams.append('SFG')
    elif year >= 1883:
        teams.append('NYG')

def marlins(year, teams):
    """ Append appropriate Marlins abbreviation for year if applicable.
    """
    if year >= 2012:
        teams.append('MIA')
    elif year >= 1993:
        teams.append('FLA')

def nationals(year, teams):
    """ Append appropriate Nationals abbreviation for year if applicable.
    """
    if year >= 2005:
        teams.append('WSN')
    elif year >= 1969:
        teams.append('MON')

def orioles(year, teams):
    """ Append appropriate Orioles abbreviation for year if applicable.
    """
    if year >= 1954:
        teams.append('BAL')
    elif year >= 1902:
        teams.append('SLB')
    elif year == 1901:
        teams.append('MLA')

def rangers(year, teams):
    """ Append appropriate Rangers abbreviation for year if applicable.
    """
    if year >= 1972:
        teams.append('TEX')
    elif year >= 1961:
        teams.append('WSA')

def rays(year, teams):
    """ Append appropriate Rays abbreviation for year if applicable.
    """
    if year >= 2008:
        teams.append('TBR')
    elif year >= 1998:
        teams.append('TBD')

def twins(year, teams):
    """ Append appropriate Twins abbreviation for year if applicable.
    """
    if year >= 1961:
        teams.append('MIN')
    elif year >= 1901:
        teams.append('WSH')

def valid_teams_subset(year, teams):
    """ Ensure teams list is valid.
    """
    all_teams = mlb_teams(int(year))
    for team in teams:
        if team not in all_teams:
            return False
    return True

