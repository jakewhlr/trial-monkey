#!/usr/bin/env python3

import argparse
import logging
import json
import asyncio
import os
import sys

from trialbot.core.bot import TrialBot

BASE_DIR = os.path.join(os.path.dirname( __file__ ))


# if os.environ["SERVER_NAME"] == "localhost":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('-c', '--config', help='config json', type=argparse.FileType('r'), required=False, default='docs/config.json')
#     parser.add_argument('-e', '--env', type=str, help='environment', choices=['production', 'staging'], required=False default='staging')
#     args = parser.parse_args()
#     CONFIG = args.config
#     ENV = args.env
# else:
CONFIG = open("./docs/config.json", "r")
ENV = "staging"

def main():
        try:
            os.system('clear')
            config = json.load(CONFIG)
            token = config[ENV]['token']
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