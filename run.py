#!/usr/bin/env python
import argparse
import automgtic
import logging

root_log = logging.getLogger()
logging.basicConfig()
root_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='automgtic - Autouploader for GNU MediaGoblin')
    parser.add_argument(
            'directory',
            type=str,
            nargs='?',
            )
    parser.add_argument(
            '--authorize',
            const=True,
            action='store_const',
            help='Initiate the configuration.')
    parser.add_argument(
            '--run',
            const=True,
            action='store_const',
            help='Run the autouploader')
    parser.add_argument(
            '--level',
            help='Logging level, one of [ CRITICAL | ERROR | WARNING | INFO | DEBUG ], default: INFO')

    args = parser.parse_args()

    root_log.setLevel(getattr(logging, args.level or 'INFO'))

    root_log.debug(args)

    if args.authorize:
        automgtic.authorize()
    if args.run:
        automgtic.run_autoupload(args.directory)
