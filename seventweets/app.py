import json

from flask import Flask
from flask import request

from seventweets import storage
from seventweets.exceptions import error_handled, NotFound, BadRequest

Storage = storage.Storage()

app = Flask(__name__)


@app.route("/tweets/", methods=["GET"])
def all_tweets():
    return json.dumps(Storage.get_all())


@app.route("/tweets/<int:tweet_id>", methods=["GET"])
@error_handled
def single_tweet(tweet_id):
    tweet = Storage.get_by_id(tweet_id)
    if tweet:
        return json.dumps(tweet)
    else:
        raise NotFound("Tweet not found")


@app.route("/tweets/", methods=["POST"])
@error_handled
def save_tweet():
    if not request.data:
        raise BadRequest("Data not sent")
    request_data = json.loads(request.data)
    if request_data['tweet']:
        Storage.save_tweet(request_data["tweet"])
        return "Tweet saved"
    else:
        raise BadRequest("Missing tweet content")


@app.route("/tweets/", methods=["DELETE"])
@error_handled
def delete_tweet():
    if not request.data:
        raise BadRequest("Data not sent")
    request_data = json.loads(request.data)
    if request_data['id']:
        if Storage.delete_tweet((int)(request_data["id"])):
            return "Tweet deleted", 204
        else:
            raise NotFound("Tweet not found")
    else:
        raise BadRequest("Missing tweet content")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
