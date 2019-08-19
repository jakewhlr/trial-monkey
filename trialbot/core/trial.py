"""
This module is used to create trials, or arguments, and track voting for
different options.
"""
import re


class Trial:


    """
    This is a class for tracking and voting on a trial or argument.

    Attributes:
        teams (dict): The teams available for voting, and lists of voters.
        title (str): The human readable title of the trial.
        description (str): A short description of the trial.
        emoji_list (list): A list of avialable emojis for voting.

    """
    def __init__(self, teams=None):
        """
        Initializes a trial with a list of teams for voting.
        
        :param teams: List of team names
        """
        self.title = " vs. ".join(i.title() for i in teams)
        self.description = ""
        self.teams = dict()
        self.teams['fence'] = {"emoji": '🤺', "votes": []}
        self.emoji_list = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣']
        for item in teams:
            self.teams[item.lower()] = {"emoji": self.emoji_list.pop(0), "votes": []}


    def __str__(self):
        """
        Returns title of trial as string.
        """
        return self.title

    def get_title(self):
        """
        Gets the current title of the trial.

        :return: Title string.
        """
        return self.title

    def vote(self, emoji, username):
        """
        Clears user from other teams and adds them to given team.

        :param emoji: Emoji character of vote.
        :param username: Username of voting user.
        :return: 0 for success, 1 for failure
        """
        for team in self.teams:
            if emoji != self.teams[team]["emoji"]:
                if username in self.teams[team]["votes"]:
                    self.teams[team]["votes"].remove(username)
            if emoji == self.teams[team]["emoji"]:
                if username in self.teams[team]["votes"]:
                    return 0
                self.teams[team]["votes"].append(username)
                return 0
        return 1

    def status(self):
        """
        Generates dict of current voting status compatible with Discord embed object.

        :return: Dict of current status.
        """
        output_dict = {"title": self.title, "description": self.description, "fields": []}
        for team in self.teams:
            inline = False if team == "fence" else True
            if len(self.teams[team]):
                value = '\n'.join(self.teams[team])
            else:
                value = '‌‌ '  # Special blank char for discord
            current_field = {
                "name": team.title(),
                "value": value,
                "inline": inline
            }
            output_dict["fields"].append(current_field)
        return output_dict


class TrialMonkey:
    """
    This is a class for tracking and voting on a multiple trials or arguments.

    Attributes:
        trials (list): A list of active trials.
        current_trial (Trial): The currently selected trial.
    """

    def __init__(self):
        """
        Initialize with default values.
        """
        self.trials = []
        self.current_trial = None

    def new_trial(self, args_string):
        """
        Creates a new trial from the arg string.

        :param args_string: String of the different sides of a trial.
                            Should be in the form Team (v | v. | vs | vs. | versus) Team.
        :return: 0 for success, nonzero for failure.
        """
        split_teams = re.split(' v | v. | vs | vs. | versus ', args_string)
        if len(split_teams) < 2:
            return 1
        self.current_trial = Trial(teams=split_teams)
        self.trials.append(self.current_trial)
        return 0

    def status(self):
        """
        Calls the status function of the current trial.

        :return: Dict of current trial's status
        """
        if not self.current_trial:
            return 1
        return self.current_trial.status()

    def list(self):
        """
        Generates a dict of available trials available for select().

        :return: Dict of titles for available trials.
        """
        output_dict = {"title": "**Available Trials**", "fields": []}
        for index, trial in enumerate(self.trials):
            if trial is self.current_trial:
                name = "**{}. {}**".format(index, trial.title)
            else:
                name = "{}. {}".format(index, trial.title)
            output_dict["fields"].append({"name": name, "value": '‌‌ '})
        return output_dict

    def select(self, index):
        """
        Sets the current trial to the given index.

        :param index: Index of the trial to switch to. From list().
        :return: 0 for success, 1 for failure.
        """
        if index < 0:
            return 1
        if index > len(self.trials):
            return 1
        self.current_trial = self.trials[index]
        return 0

    def vote(self, emoji, username):
        """
        Places a vote on the current trial.

        :param emoji: Emoji character for vote.
        :param username: Username string of voting user.
        :return: 0 for success, 1 for failure.
        """
        if not self.current_trial:
            return 1
        return self.current_trial.vote(emoji, username)

    def adjourn(self):
        """
        Ends the current trial.

        :return: 0 for success, 1 for failure
        """
        if not self.current_trial:
            return 1
        self.trials.remove(self.current_trial)
        self.current_trial = None
        return 0