import pytest
from trialbot.core.bot import TrialBot

class TestTrialBot(object):
	def test_init(self):
		test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")
		assert test_bot.token == "afj34q9opf8ihaf44f8hasef"

	def test_valid_reaction(self):
		test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")

		del test_bot

	def test_set_command_prefix(self):
		test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")
		assert test_bot.bot.command_prefix == '!'
		test_bot.set_command_prefix("test_command_prefix")
		assert test_bot.bot.command_prefix == "test_command_prefix"
		del test_bot

	# def test_bot_reacton_add(self):
	# 	test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")
	# 	bot_user_id = 1
	# 	status_message_id = 16239874
	# 	reaction_info = {
	# 		"message_id": 0,
	# 		"message_author_id": 1234,
	# 		"emoji": "1⃣"
	# 	}
	# 	response_code = test_bot.bot_on_reaction_add(bot_user_id, status_message_id, reaction_info)
	# 	assert response_code == 0