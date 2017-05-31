if __name__ == "__main__":
    import sys

    if sys.argv[1] == "storage":
        from seventweets import storage
        Storage = storage.Storage()
        Storage.bootstrap()
        if len(sys.argv) == 3:
            Storage.add_api_key(sys.argv[2])
    else:
        from seventweets import app
        app.run(host="0.0.0.0")
