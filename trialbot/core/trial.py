import logging
import tabulate
from pyfiglet import figlet_format
import discord
import json

class Trial:
	left_name = ''
	right_name = ''
	name = ''
	standings = {}
	votes = {}
	status_message = None
	def __init__(self, options):
		self.votes['fence'] = []
		for item in options:
			self.votes[item.lower()] = []
		self.description = ""

	def __str__(self):
		return self.name

	def vote(self, team, username):
		team = team.lower()
		if team not in self.votes:
			return 1
		elif username in self.votes[team]:
			return 0
		else:
			for current_team in self.votes.keys():
				if username in self.votes[current_team]:
					self.votes[current_team].remove(username)
			self.votes[team].append(username)
			return 0

	def status(self):
		output = {}
		title = ""
		for item in self.votes.keys():
			if item != "fence":
				title = title + "%s vs. " % item.title()
		if title.endswith(" vs. "):
			title = title[:-5]
		output['title'] = title
		output['description'] = self.description
		output['votes'] = self.votes
		return output