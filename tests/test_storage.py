import pytest
from seventweets import storage

Storage = storage.Storage()
try:
    Storage.bootstrap()
except:
    pass

def test_fetch_all_tweets():
    allTweets = Storage.get_all()
    assert type(allTweets) == list
    for tweet in allTweets:
        assert type(tweet) == dict
        assert "id" in tweet
        assert "tweet" in tweet


def test_add_tweet():
    initialLen = len(Storage.get_all())
    newTweet = Storage.save_tweet("test")
    assert type(Storage.get_all()) == list
    assert len(Storage.get_all()) - initialLen == 1
    assert type(newTweet) == dict
    assert "id" in newTweet
    assert "tweet" in newTweet


def test_fetching_by_id():
    newTweet = Storage.save_tweet("test")
    tweet = Storage.get_by_id(newTweet['id'])
    assert type(tweet) == dict
    assert "id" in tweet
    assert "tweet" in tweet
    assert tweet["id"] == newTweet['id']


def test_delete():
    newTweet = Storage.save_tweet("test")
    Storage.delete_tweet(newTweet['id'])
    assert not Storage.get_by_id(newTweet['id'])



