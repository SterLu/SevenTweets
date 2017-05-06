from fabric.api import local, settings


def initial_setup():
    with settings(warn_only=True):
        local('docker network create radionica')
        start_storage()


def build():
    local('git pull origin master')
    with settings(warn_only=True):
        local('docker stop seventweets-container')
        local('docker rmi seventweets-image')
    local('docker build -t seventweets-image .')


def start():
    local('docker run --rm -d --net radionica -p 8000:8000 --name seventweets-container seventweets-image')


def deploy():
    build()
    start()


def full_deploy():
    initial_setup()
    deploy()


def stop():
    local('docker stop seventweets-container')


def clear():
    local('docker stop seventweets-container')
    local('docker rmi seventweets-image')


def start_storage():
    local('docker run -d --name storage-container --net radionica --restart unless-stopped -e POSTGRES_USER=radionica -e POSTGRES_PASSWORD=P4ss -v radionica-postgres-data:/var/lib/postgresql/data -p 127.0.0.1:5432:5432 postgres:9.6.2')
