#! /usr/bin/env python3
import argparse

import BrefScraper as brf
import Plot as plot

parser = argparse.ArgumentParser()
parser.add_argument('plot_type',
                    choices=plot.OPTIONS.keys(),
                    type=str,
                    help='Data type requesting to plotted.')
parser.add_argument('-a',
                    '--average',
                    action='store_true',
                    help='Calculate and plot the average for teams selected.')
parser.add_argument('-n',
                    '--not-histogram',
                    action='store_true',
                    help='Set flag if histogram is not desired, data is linearly aggragated by '
                         'x. (default: %(default)s)')
parser.add_argument('-p',
                    '--playoffs',
                    action='store_true',
                    help='Set flag if including playoffs is desired. '
                         '(default: %(default)s)')
group = parser.add_mutually_exclusive_group()
group.add_argument('-t',
                   '--teams',
                   type=str,
                   choices=['AL', 'NL', 'MLB'],
                   help='List of teams by League or all.')
group.add_argument('-c',
                   '--teams-custom',
                   type=str,
                   metavar='TEAM',
                   nargs='+',
                   dest='teams',
                   help='List of teams to get information from, use Baseball-Reference '
                        'abreviations. Append " -- " after list to seperate from '
                        'positional argument, when immediately following.')
parser.add_argument('-x',
                    '--x-hint',
                    type=int,
                    default=10,
                    metavar='X-MAX',
                    help='The minimum x-axis value end point in [1, x]; value will be '
                         'increased as needed. (default: %(default)s)')
parser.add_argument('-y',
                    '--year',
                    type=int,
                    default=2015,
                    help='Desired target year for data sets to retrieve. '
                         '(default: %(default)s)')
parser.add_argument('--y-axis',
                    type=int,
                    nargs=2,
                    dest='y_axis',
                    default=[-24, 24],
                    metavar='Y',
                    help='Min and max for y-axis (default: %(default)s)')

def main():
    """ Collect data and plot as required from arguments.
    """
    args = parser.parse_args()
    if isinstance(args.teams, str):
        args.teams = brf.__getattribute__(args.teams)
    scraper = brf.BrefScraper(args.teams, str(args.year), args.playoffs)
    plotter = plot.Plot(scraper, not args.not_histogram)
    plotter.set_default_axes(1, args.x_hint, args.y_axis[0], args.y_axis[1])
    plotter.plot(args.plot_type, args.average)

if __name__ == '__main__':
    main()
