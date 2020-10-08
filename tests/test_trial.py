"""
Test cases for methods of trialbot.trial.Trial.
"""
from src.trialbot.trial import Trial

def test_initialize():
    """
    Initializes new trial, checks for votes structure.
    """
    test_trial = Trial(teams=["good", "evil"])
    assert test_trial.title == "Good vs. Evil"
    assert test_trial.get_teams() == ["fence", "good", "evil"]
    assert test_trial.teams["fence"]["votes"] == []
    assert test_trial.teams["good"]["votes"] == []
    assert test_trial.teams["evil"]["votes"] == []

def test_vote():
    """
    Tests stages of voting and vote changing.
    """
    test_trial = Trial(teams=["good", "evil"])

    test_trial.vote('1⃣', "Luke")
    assert test_trial.get_votes("good") == ["Luke"]

    test_trial.vote('2⃣', "Vader")
    assert test_trial.get_votes("evil") == ["Vader"]

    test_trial.vote('1⃣', "Vader")
    assert test_trial.get_votes("good") == ["Luke", "Vader"]
    assert test_trial.get_votes("evil") == []


def test_rename():
    """
    Test renaming of trial team
    :return:
    """
    rename_trial = Trial(["good", "evil"])

    return_code = rename_trial.rename("gooood", "neutral")
    assert return_code == 1
    assert rename_trial.get_teams() == ["fence", "good", "evil"]

    return_code = rename_trial.rename("good", "neutral")
    assert return_code == 0
    assert rename_trial.get_teams() == ["fence", "evil", "neutral"]