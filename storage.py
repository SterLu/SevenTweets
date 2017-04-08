class Storage:
    _tweets = []

    def __init__(self):
        print("init")
        self._tweets = [{
            "id": 1,
            "name": "test",
            "tweet": "this is a tweet"
        }]
        self._last_id = 1

    def get_all(self):
        return self._tweets

    def get_by_id(self, tweet_id):
        for i, tweet in self._tweets:
            if tweet['id'] == tweet_id:
                return tweet
        else:
            return False

    def save_tweet(self, tweet_text):
        self._tweets.append({
            "id": self._last_id + 1,
            "name": "test",
            "tweet": tweet_text
        })
        self._last_id += 1

    def delete_tweet(self, tweet_id):
        index = 0
        for tweet in self._tweets:
            if tweet['id'] == tweet_id:
                del self._tweets[index]
                return True
            index += 1
        else:
            return False
