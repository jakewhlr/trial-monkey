#!/usr/bin/env python3

import argparse
import logging
import json
import asyncio
import os
import sys

from core.bot import TrialBot

BASE_DIR = os.path.join(os.path.dirname( __file__ ))

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--config', help='config json', type=argparse.FileType('r'), required=True)
parser.add_argument('-e', '--env', type=str, help='environment', choices=['production', 'staging'], default='production')

args = parser.parse_args()

def main():
        try:
            os.system('clear')
            config = json.load(args.config)
            token = config[args.env]['token']
            print(token)
            bot = TrialBot(token)
            loop = asyncio.get_event_loop()
            loop.run_until_complete(bot.start())
            # loop.run_until_complete(bot.stop())
            loop.close()
        except KeyboardInterrupt:
            print('Exiting')
        finally:
            del bot
            try:
                sys.exit(0)
            except SystemExit:
                os._exit(0)


if __name__ == '__main__':
       main()