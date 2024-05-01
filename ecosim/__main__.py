from argparse import ArgumentParser
from pathlib import Path
from sys import exc_info as get_exception_info
from traceback import print_tb as print_traceback

from constants import DAYS_PER_YEAR
from simulation import Simulation
from util import CustomException


def main(args):
    simulation = Simulation(args.start_file)

    simulation.start()

    for day in range(args.days):
        print(f"Day {day + 1} / {args.days}")
        simulation.next_day()

    simulation.finish()


def parseArgs():
    parser = ArgumentParser(description="")
    parser.add_argument("start_file", metavar="start-file", type=Path)
    parser.add_argument("-d", "--days", default=DAYS_PER_YEAR, type=int)
    return parser.parse_args()


if __name__ == "__main__":
    try:
        main(parseArgs())
    except CustomException as error:
        print("{}: {}".format(type(error).__name__, str(error)))
        print("Exiting...")
        exit()
    except Exception as error:
        print("{}: {}".format(type(error).__name__, str(error)))
        print("Traceback:")
        print_traceback(get_exception_info()[2])
        print("Exiting...")
        exit()
