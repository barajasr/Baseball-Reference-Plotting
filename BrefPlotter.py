#! /usr/bin/env python3
import argparse

import BrefScraper as brf
import Plot as plot

parser = argparse.ArgumentParser()
parser.add_argument('--csv-dump',
                    action='store_true',
                    help='Set flag to store all table data in local csv files.'
                         ' (default: %(default)s)')
parser.add_argument('-p',
                    '--playoffs',
                    action='store_true',
                    help='Set flag if including playoffs is desired. '
                         '(default: %(default)s)')
team_select = parser.add_mutually_exclusive_group(required=True)
team_select.add_argument('-t',
                         '--teams',
                         type=str,
                         choices=['AL', 'NL', 'MLB'],
                         help='List of teams by League or all.')
team_select.add_argument('-c',
                         '--teams-custom',
                         type=str,
                         metavar='TEAM',
                         nargs='+',
                         dest='teams',
                         help='List of teams to get information from, use '
                               'Baseball-Reference abreviations.')
parser.add_argument('-y',
                    '--year',
                    type=int,
                    default=2015,
                    help='Desired target year for data sets to retrieve. '
                         '(default: %(default)s)')
plot_group = parser.add_argument_group('Plotting')
plot_group.add_argument('--csv-read',
                        action='store_true',
                        help='Read data from local csv files.'
                             ' (default: %(default)s)')
plot_group.add_argument('--plot',
                        choices=plot.OPTIONS.keys(),
                        type=str,
                        default='',
                        help='Data type requesting to plotted.')
plot_group.add_argument('-a',
                        '--average',
                        action='store_true',
                        help='Calculate and plot the average for teams selected.')
plot_group.add_argument('-n',
                        '--not-histogram',
                        action='store_true',
                        help='Set flag if histogram is not desired, data is linearly '
                             'aggragated by x. (default: %(default)s)')
plot_group.add_argument('-x',
                        '--x-hint',
                        type=int,
                        default=10,
                        metavar='X-MAX',
                        help='The minimum x-axis value end point in [1, x]; value '
                             'will be increased as needed. (default: %(default)s)')
plot_group.add_argument('--y-axis',
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
    if args.csv_read and args.csv_dump:
        raise Exception('Reading and writing from bsv at the same time is silly')

    scraper = brf.BrefScraper(args.teams,
                              str(args.year),
                              args.playoffs,
                              args.csv_read)

    if not args.csv_dump and args.plot != '':
        plotter = plot.Plot(scraper, not args.not_histogram)
        plotter.set_default_axes(1, args.x_hint, args.y_axis[0], args.y_axis[1])
        plotter.plot(args.plot, args.average)
    elif args.csv_dump and args.plot == '':
        scraper.save_to_file()

if __name__ == '__main__':
    main()
