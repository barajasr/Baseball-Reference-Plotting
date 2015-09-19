# Baseball-Reference-Plotting
```
usage: BrefPlotter.py [-h] [-n] [-p] [-t {AL,NL,MLB} | -tc TEAM [TEAM ...]]
                      [-x X_HINT] [-y YEAR] [--y-axis Y Y]
                      {win_loss_streaks,win_loss_margins,outcome_scoring,outcome_conceding}

positional arguments:
  {win_loss_streaks,win_loss_margins,outcome_scoring,outcome_conceding}
                        Data type requesting to plotted.

optional arguments:
  -h, --help            show this help message and exit
  -n, --not-histogram   Set flag if histogram is not desired, data is linearly
                        aggragated by x. (default: False)
  -p, --playoffs        Set flag if including playoffs is desired. (default:
                        False)
  -t {AL,NL,MLB}, --teams {AL,NL,MLB}
                        List of teams by League or all.
  -tc TEAM [TEAM ...], --teams-custom TEAM [TEAM ...]
                        List of teams to get information from, use Baseball-
                        Reference abreviations. Append " -- " after list to
                        seperate from positional argument, when immediately
                        following.
  -x X_HINT, --x-hint X_HINT
                        The minimum x-axis value end point in [1, x]; value
                        will be increased as needed. (default: 10)
  -y YEAR, --year YEAR  Desired target year for data sets to retrieve.
                        (default: 2015)
  --y-axis Y Y          Min and max for y-axis (default: [-24, 24])
```
