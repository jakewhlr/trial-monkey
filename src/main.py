#!/usr/bin/env python3
"""
Main script to start Trial Monkey.
"""

import argparse
import json
import asyncio
import os

from trialbot.bot import TrialBot

BASE_DIR = os.path.join(os.path.dirname(__file__))

PARSER = argparse.ArgumentParser()
PARSER.add_argument('-c', '--config', help='config json',
                                        type=argparse.FileType('r'), required=True)
PARSER.add_argument('-e', '--env', type=str, help='environment',
                                        choices=['production', 'staging'], required=False,
                                        default='production')
ARGS = PARSER.parse_args()


def main():
    """
    Loads config file, initializes TrialBot.
    """
    try:
        os.system('clear')
        config = json.load(ARGS.config)
        token = config[ARGS.env]['token']
        bot = TrialBot(token)
        loop = asyncio.get_event_loop()
        loop.run_until_complete(bot.start())
        loop.close()
    except KeyboardInterrupt:
        print('Exiting')


if __name__ == '__main__':
    main()
