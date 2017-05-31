if __name__ == "__main__":
    import sys

    if sys.argv[1] == "storage":
        if len(sys.argv) < 3:
            print("Usage: python -m seventweets storage [api-key]")
            exit()
        from seventweets import storage
        Storage = storage.Storage()
        Storage.bootstrap(sys.argv[2])
    else:
        from seventweets import app
        app.run(host="0.0.0.0")
