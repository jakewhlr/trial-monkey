import pytest
import json
from trialbot.core.trial import Trial

class TestTrial(object):
	def test_initialize(self):
		test_trial = Trial(["good", "evil"])
		assert test_trial.votes == {
			"good": [],
			"evil": [],
			"fence": []
		}

	def test_vote(self):
		test_trial = Trial(["good", "evil"])
		test_trial.vote("good", "Luke")
		assert test_trial.votes == {"good": ["Luke"], "fence": [], "evil": []}
		test_trial.vote("evil", "Vader")
		assert test_trial.votes == {"good": ["Luke"], "fence": [], "evil": ["Vader"]}
		test_trial.vote("good", "Vader")
		assert test_trial.votes == {"good": ["Luke", "Vader"], "fence": [], "evil": []}


	def test_status(self):
		test_trial = Trial(["good", "evil"])
		expected_output = {
			"title": "Good vs. Evil",
			"description": "",
			"votes": {
				"good": [],
				"fence": [],
				"evil": []
			}
		}
		assert test_trial.status() == expected_output
		test_trial.vote("good", "Luke")
		expected_output = {
			"title": "Good vs. Evil",
			"description": "",
			"votes": {
				"good": ["Luke"],
				"fence": [],
				"evil": []
			}
		}
		assert test_trial.status() == expected_output
		test_trial.vote("evil", "Vader")
		expected_output = {
			"title": "Good vs. Evil",
			"description": "",
			"votes": {
				"good": ["Luke"],
				"fence": [],
				"evil": ["Vader"]
			}
		}
		assert test_trial.status() == expected_output
		test_trial.vote("fence", "Vader")
		test_trial.vote("good", "Vader")
		expected_output = {
			"title": "Good vs. Evil",
			"description": "",
			"votes": {
				"good": ["Luke", "Vader"],
				"fence": [],
				"evil": []
			}
		}
		assert test_trial.status() == expected_output