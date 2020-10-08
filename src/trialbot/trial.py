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
            self.teams[item.lower()] = {
                "emoji": self.emoji_list.pop(0),
                "votes": []
            }

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

    def get_emoji(self):
        """
        Gets a list of currently used emoji.

        :return: List of emoji chars.
        """
        output_list = list()
        for team in self.teams:
            output_list.append(self.teams[team]["emoji"])
        return output_list

    def get_teams(self):
        """
        Gets a list of teams.

        :return: List of teams.
        """
        return list(self.teams.keys())

    def get_votes(self, team):
        """
        Gets a list of votes for a given team.

        :param team: Team name to get votes from.
        :return: List of users.
        """
        if team not in self.teams.keys():
            return None
        return self.teams[team]["votes"]

    def vote(self, emoji, username):
        """
        Clears user from other teams and adds them to given team.

        :param emoji: Emoji character of vote.
        :param username: Username of voting user.
        :return: 0 for success, 1 for failure
        """
        for team in self.teams:
            if username in self.teams[team]["votes"]:
                self.teams[team]["votes"].remove(username)
            if emoji == self.teams[team]["emoji"]:
                self.teams[team]["votes"].append(username)

    def status(self):
        """
        Generates dict of current voting status compatible with Discordembed
        object.

        :return: Dict of current status.
        """
        output_dict = {
            "title": self.title,
            "description": self.description,
            "fields": []
        }
        for team in self.teams:
            if team == "fence":
                name = "The Fence"
                value = ', '.join(self.teams[team]["votes"])
                inline = False
            else:
                name = team.title()
                inline = True
                value = '\n'.join(self.teams[team]["votes"])
            current_field = {
                "name": self.teams[team]["emoji"] + ' ' + name,
                "value": value + "\n\u200b",
                "inline": inline
            }
            output_dict["fields"].append(current_field)
        return output_dict

    def rename(self, old_name, new_name):
        """
        Renames team old_name to new_name if old_name exists.

        :param old_name: Name of team to rename.
        :param new_name: Name to rename to.
        :return: 0 for success, 1 for failure
        """
        if not old_name.lower() in self.teams.keys():
            return 1

        self.teams[new_name.lower()] = self.teams.pop(old_name.lower())
        return 0


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

    def get_emoji(self):
        """
        Gets list of used emoji from current trial.

        :return: List of emoji.
        """
        if not self.current_trial:
            return None
        return self.current_trial.get_emoji()

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
        index = int(index)
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

    def rename(self, old_name, new_name):
        """
        Renames team old_name to new_name if old_name exists in current trial.

        :param old_name: Name of team to rename.
        :param new_name: Name to rename to.
        :return: 0 for success, 1 for failure
        """
        return self.current_trial.rename(old_name, new_name)
