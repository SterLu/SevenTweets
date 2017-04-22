import pytest
from seventweets import storage

Storage = storage.Storage()


def test_initial():
    assert hasattr(Storage, "_tweets")
    assert hasattr(Storage, "_last_id")
    assert type(Storage._tweets) == list
    assert type(Storage._last_id) == int

def test_fetch_all_tweets():
    allTweets = Storage.get_all()
    assert type(allTweets) == list
    assert len(allTweets) == len(Storage._tweets)
    for tweet in allTweets:
        assert type(tweet) == dict
        assert "id" in tweet
        assert "tweet" in tweet
        assert "name" in tweet


def test_add_tweet():
    initialLen = len(Storage.get_all())
    initialLastId = Storage._last_id
    Storage.save_tweet("test")
    assert type(Storage.get_all()) == list
    assert len(Storage.get_all()) - initialLen == 1
    assert initialLastId + 1 == Storage._last_id
    assert Storage.get_all()[initialLastId]["tweet"] == "test"


def test_fetching_by_id_simple():
    Storage.save_tweet("test")
    tweet = Storage.get_by_id(1)
    assert type(tweet) == dict
    assert "id" in tweet
    assert "tweet" in tweet
    assert "name" in tweet
    assert tweet["id"] == 1


def test_delete():
    initialLastId = Storage._last_id
    Storage.save_tweet("test")
    Storage.delete_tweet(initialLastId)
    assert not Storage.get_by_id(initialLastId)


def test_fetching_by_id():
    initialLastId = Storage._last_id
    Storage.save_tweet("test")
    Storage.save_tweet("test 2")
    Storage.delete_tweet(initialLastId)
    assert not Storage.get_by_id(initialLastId)
    tweet = Storage.get_by_id(initialLastId + 1)
    assert type(tweet) == dict
    assert "id" in tweet
    assert "tweet" in tweet
    assert "name" in tweet
    assert tweet["id"] == initialLastId + 1


