import json

from flask import Flask
from flask import request

from seventweets import storage
from seventweets.exceptions import error_handled, NotFound, BadRequest

Storage = storage.Storage()
Nodes = storage.Nodes()

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


@app.route("/search/<query>", methods=["GET"])
@error_handled
def search(query):
    return json.dumps(Storage.search(query))


@app.route("/join_network/", methods=["POST"])
@error_handled
def join_network():
    if not request.data:
        raise BadRequest("Data not sent")
    request_data = json.loads(request.data)
    if request_data['name'] and request_data['address']:
        print("Initializing current node as '" + request_data['name'] + "' at " + request_data['address'])
        Nodes.set_self(request_data['name'], request_data['address'])
        return "Joined"
    else:
        raise BadRequest("Missing parameters")


@app.route("/network_status/", methods=["GET"])
@error_handled
def network_status():
    return json.dumps(Nodes.get_all())


@app.route("/register/", methods=["POST"])
@error_handled
def register_node():
    if not request.data:
        raise BadRequest("Data not sent")
    request_data = json.loads(request.data)
    if request_data['name'] and request_data['address']:
        self_data = Nodes.get_self()
        if self_data:
            print("New node '" + request_data['name'] + "' at " + request_data['address'])
            Nodes.register_node(request_data['name'], request_data['address'])
            return json.dumps(Nodes.get_all_external())
        else:
            raise NotFound("Network not joined")
    else:
        raise BadRequest("Missing parameters")


@app.route("/register/<node_name>", methods=["DELETE"])
@error_handled
def delete_node(node_name):
    self_data = Nodes.get_self()
    if self_data:
        Nodes.delete_node(node_name)
        return "", 204
    else:
        raise NotFound("Network not joined")


if __name__ == "__main__":
    app.run(host="0.0.0.0")
