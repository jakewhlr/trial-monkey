import pytest
import json
from trialbot.core.trial import Trial

class TestTrial(object):
	def test_initialize(self):
		test_trial = Trial("good", "evil")
		assert test_trial.left_name == "Good"
		assert test_trial.right_name == "Evil"
		assert test_trial.name == "Good v. Evil"

	def test_status(self):
		# TODO
		assert True

	def test_toJSON(self):
		test_trial = Trial("good", "evil")
		output_json = test_trial.toJSON()
		expected_json = json.dumps({
			"name": "Good v. Evil",
			"id": 0,
			"left_name": "Good",
			"right_name": "Evil",
			"standings": {
				"left": [],
				"fence": [],
				"right": []
			}
		})
		assert output_json == expected_json