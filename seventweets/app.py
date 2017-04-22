import json

from flask import Flask
from flask import request

from seventweets import storage

Storage = storage.Storage()

app = Flask(__name__)


@app.route("/tweets/", methods=["GET"])
def all_tweets():
    return json.dumps(Storage.get_all())


@app.route("/tweets/<int:tweet_id>", methods=["GET"])
def single_tweet(tweet_id):
    tweet = Storage.get_by_id(tweet_id)
    if tweet:
        return json.dumps(tweet)
    else:
        return "Tweet not found", 404


@app.route("/tweets/", methods=["POST"])
def save_tweet():
    if not request.data:
        return "Data not sent", 400
    request_data = json.loads(request.data)
    if request_data['tweet']:
        Storage.save_tweet(request_data["tweet"])
        return "Tweet saved"
    else:
        return "Missing tweet content", 400


@app.route("/tweets/", methods=["DELETE"])
def delete_tweet():
    if not request.data:
        return "Data not sent", 400
    request_data = json.loads(request.data)
    if request_data['id']:
        if Storage.delete_tweet((int)(request_data["id"])):
            return "Tweet deleted", 204
        else:
            return "Tweet not found", 400
    else:
        return "Missing tweet content", 400


if __name__ == "__main__":
    app.run(host="0.0.0.0")
    print("Server started. ")
