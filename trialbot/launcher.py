#!/usr/bin/env python3
import sys
import os
import threading
import pyfiglet
import asyncio

from core.bot import TrialBot

class Menu:
    def __init__(self):
        self.status = 'offline'
        self.choices = {
            '1': self.start_bot,
            '2': self.stop_bot,
            '3': self.exit,
        }

    def print_menu(self):
        title = pyfiglet.figlet_format('TrialBot', font='banner')
        version_info = 'TrialBot version %s' % '0.0.1'
        if self.status == 'online':
            status_strings = [self.status]
            if len(self.bot.client.guilds) is not 0:
                status_strings.append(self.bot.client.guilds)
            if self.bot.client.user:
                status_strings.append(self.bot.client.user)
            status_string = ''.join(status_strings)
            print(status_string)
        elif self.status == 'offline':
            status_string = self.status


        status_string = 'Status: %s' % self.status
        menu_entries = '\n'.join([
            '1. Start bot',
            '2. Stop bot',
            '3. Exit'
        ])
        # os.system('clear')

        print(title)
        print(version_info)
        print(status_string)
        print(30 * '-' , 'MENU' , 30 * '-')
        print(menu_entries)
        print(67 * '-')

    def run(self):
        while True:
            self.print_menu()
            choice = input('Enter an option: ')
            choice_function = self.choices.get(choice)
            if choice_function:
                choice_function()
            else:
                print('Invalid option')

    def start_bot(self):
        token = input('Secret token:')
        self.bot = TrialBot(token)
        # bot_thread = threading.Thread(target=self.bot.start)
        # bot_thread.start()
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.bot.start())
        loop.close()
        self.status = 'online'
        return

    def stop_bot(self):
        print('Stopping bot...')
        return
    def exit(self):
        sys.exit(0)

def main():
    Menu().run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Exiting')
