# Baseball-Reference-Plotting
```
usage: BrefPlotter.py [-h] [--csv-dump] [-p]
                      (-t {AL,NL,MLB} | -c TEAM [TEAM ...]) [-y YEAR]
                      [--csv-read]
                      [--plot {outcome_conceding,outcome_scoring,win_loss_streaks,win_loss_margins}]
                      [-a] [-n] [-x X-MAX] [--y-axis Y Y]

optional arguments:
  -h, --help            show this help message and exit
  --csv-dump            Set flag to store all table data in local csv files.
                        (default: False)
  -p, --playoffs        Set flag if including playoffs is desired. (default:
                        False)
  -t {AL,NL,MLB}, --teams {AL,NL,MLB}
                        List of teams by League or all.
  -c TEAM [TEAM ...], --teams-custom TEAM [TEAM ...]
                        List of teams to get information from, use Baseball-
                        Reference abreviations.
  -y YEAR, --year YEAR  Desired target year for data sets to retrieve.
                        (default: 2015)

Plotting:
  --csv-read            Read data from local csv files. (default: False)
  --plot {outcome_conceding,outcome_scoring,win_loss_streaks,win_loss_margins}
                        Data type requesting to plotted.
  -a, --average         Calculate and plot the average for teams selected.
  -n, --not-histogram   Set flag if histogram is not desired, data is linearly
                        aggragated by x. (default: False)
  -x X-MAX, --x-hint X-MAX
                        The minimum x-axis value end point in [1, x]; value
                        will be increased as needed. (default: 10)
  --y-axis Y Y          Min and max for y-axis (default: [-24, 24])
```
