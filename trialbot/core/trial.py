"""
This module is used to create trials, or arguments, and track voting for
different options.
"""


class Trial:
    """
    This is a class for tracking and voting on trials or arguments.

    Attributes:
        votes (dict): The teams available for voting, and lists of voters.
        title (str): The human readable title of the trial.
        description (str): A short description of the trial.

    """

    title = None
    description = None
    votes = {}
    status_message = None

    def __init__(self, teams=None):
        """
        Initializes a trial with a list of teams for voting.

        Keyword arguments:
            options (list): List of team names.
        """
        self.title = " vs. ".join(i.title() for i in teams)
        self.description = ""
        self.votes = {}
        self.votes['fence'] = []
        for item in teams:
            self.votes[item.lower()] = []

    def __str__(self):
        """
        Returns title of trial as string.
        """
        return self.title

    def vote(self, team, username):
        """
        Clears user from other teams and adds them to given team.

        Keyword arguments:
            team (str): the team to vote for
            user (str): the username of the voter
        """
        team = team.lower()
        if team not in self.votes:
            return 1
        if username in self.votes[team]:
            return 0
        for current_team in self.votes:
            if username in self.votes[current_team]:
                self.votes[current_team].remove(username)
        self.votes[team].append(username)
        return 0

    def status(self):
        """
        Returns dict detailing the title, description, and current standings.
        """
        output = {}
        self.title = ""
        for item in self.votes:
            if item != "fence":
                self.title = self.title + "%s vs. " % item.title()
        if self.title.endswith(" vs. "):
            self.title = self.title[:-5]
        output['title'] = self.title
        output['description'] = self.description
        output['votes'] = self.votes
        return output
