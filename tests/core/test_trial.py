"""
Test cases for methods of trialbot.core.trial.Trial.
"""

from trialbot.core.trial import Trial


def test_initialize():
    """
    Initializes new trial, checks for votes structure.
    """
    test_trial = Trial(teams=["good", "evil"])
    assert test_trial.title == "Good vs. Evil"
    assert test_trial.votes == {
        "good": [],
        "evil": [],
        "fence": []
    }


def test_vote():
    """
    Tests stages of voting and vote changing.
    """
    test_trial = Trial(teams=["good", "evil"])
    test_trial.vote("good", "Luke")
    assert test_trial.votes == {
        "good": ["Luke"],
        "fence": [],
        "evil": []
    }
    test_trial.vote("evil", "Vader")
    assert test_trial.votes == {
        "good": ["Luke"],
        "fence": [],
        "evil": ["Vader"]
    }
    test_trial.vote("good", "Vader")
    assert test_trial.votes == {
        "good": ["Luke", "Vader"],
        "fence": [],
        "evil": []
    }


def test_status():
    """
    Tests initial status, and status after voting.
    """
    test_trial = Trial(teams=["good", "evil"])
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
