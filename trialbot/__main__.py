#!/usr/bin/env python3

import logging
import json

import core.bot

def main():
        with open('config.json', 'r') as f:
            config = json.load(f)
        print("starting bot...")
        core.bot.start(config['token'])

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
