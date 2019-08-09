import pytest
import re
from trialbot.core.bot import TrialBot

class TestTrialBot(object):
	def test_init(self):
		test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")
		assert test_bot.token == "afj34q9opf8ihaf44f8hasef"

	def test_set_command_prefix(self):
		test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")
		assert test_bot.bot.command_prefix == '!'
		test_bot.set_command_prefix("test_command_prefix")
		assert test_bot.bot.command_prefix == "test_command_prefix"
		del test_bot

	def test_check_valid_reaction(self):
		test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")

		# TODO - Write bot.new_trial() function + test
		# Test case 4 depends ^

		# Test case 1: Message reacted != status message
		response = test_bot.check_valid_reaction(
			bot_user_id = 1234,
			status_message_id = 169851,
			message_id = 19681,
			user_id = 6514,
			emoji = '1⃣'
		)
		assert response == False

		# Test case 2: Bot user == reacting user
		response = test_bot.check_valid_reaction(
			bot_user_id = 1234,
			status_message_id = 169851,
			message_id = 169851,
			user_id = 1234,
			emoji = '1⃣'
		)
		assert response == False

		# Test case 3: Emoji not in assigned_emoji
		response = test_bot.check_valid_reaction(
			bot_user_id = 1234,
			status_message_id = 169851,
			message_id = 169851,
			user_id = 12345,
			emoji = '😎'
		)
		assert response == False

		# Test case 4: All parameters pass
		response = test_bot.check_valid_reaction(
			bot_user_id = 1234,
			status_message_id = 19681,
			message_id = 19681,
			user_id = 12345,
			emoji = '1⃣'
		)
		assert response == True

	def test_split_args(self):
		test_bot = TrialBot("afj34q9opf8ihaf44f8hasef")

		output = test_bot.split_args("One v. Two")
		assert output == ["One", "Two"]

		output = test_bot.split_args("One v. Two v Three")
		assert output == ["One", "Two", "Three"]

		output = test_bot.split_args("One versus Two vs. three")
		assert output == ["One", "Two", "three"]

		output = test_bot.split_args("One")
		assert output == None