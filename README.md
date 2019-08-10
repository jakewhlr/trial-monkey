# Trial Monkey

Trial Monkey is a Discord bot for facilitating arguments.

## Getting Started
To run the bot locally, create a python virtual environment to install dependencies.  
`python -m virtualenv -p python3 /path/to/virtualenv`
Activate the virtual environment  
`source /path/to/virtualenv/bin/activate`
Install dependencies  
`pip install -r requirements.txt`
Run application. See usage section below for command line usage.  
`./main.py -c config.json -e production`

## Config
A JSON configuration file is required containing a Discord bot token. The config supports several different tokens for different environments, the default selection is "production", so that is required. Example:
```json
{
        "production" : {
            "token": "MjkyNDA1MzczODMzMzE0MzA0.XU5mXQ.KCGXNijoVsGU0WVxZ5FUARfCUGY"
        },

        "staging" : {
            "token": "MjkyNDA1MzczODMzMzE0MzA0.XU5mbg.V-G35f81GX5UPpEDYSSyl0TE4CM"
        }
}
```

## Usage
### Running via command line
```
usage: main.py [-h] -c CONFIG [-e {production,staging}]

optional arguments:
  -h, --help            show this help message and exit
  -c CONFIG, --config CONFIG
                        config json
  -e {production,staging}, --env {production,staging}
                        environment
```
### Using in Discord
Command prefix is a mention of the bot user (ex: "@Trial Monkey#5432 gif")
### Bot Commands
```
No Category:
  adjourn
  boomer
  gif     Sends mokney gif
  help    Shows this message
  new     Creates new trial
  save
  status  Shows status of given trial (default=current)

Type @Trial Monkey help command for more info on a command.
You can also type @Trial Monkey help category for more info on a category.
```
Arguments for a new trial are delimited by ('v', 'v.', 'vs', 'vs.', 'versus') (ex: `@Trial Monkey#5432 new Good v. Evil`)

## License
[MIT](https://choosealicense.com/licenses/mit/)
