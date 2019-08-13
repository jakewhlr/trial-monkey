import logging
import tabulate
from pyfiglet import figlet_format
import discord
import json

class Trial:
	left_name = ''
	right_name = ''
	title = ''
	standings = {}
	votes = {}
	status_message = None
	def __init__(self, options):
		self.votes = {}
		self.votes['fence'] = []
		for item in options:
			self.votes[item.lower()] = []
		self.description = ""

	def __str__(self):
		return self.title

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
		self.title = ""
		for item in self.votes.keys():
			if item != "fence":
				self.title = self.title + "%s vs. " % item.title()
		if self.title.endswith(" vs. "):
			self.title = self.title[:-5]
		output['title'] = self.title
		output['description'] = self.description
		output['votes'] = self.votes
		return output