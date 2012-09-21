import argparse
import automgtic

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='automgtic - Autouploader for GNU MediaGoblin')
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

    args = parser.parse_args()

    if args.authorize:
        automgtic.authorize()
