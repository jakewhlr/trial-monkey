#!/usr/bin/env python3

import logging
import json

from core.bot import trialbot

def main():
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("starting bot...")
        bot = trialbot(config['token'])
        bot.start()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
