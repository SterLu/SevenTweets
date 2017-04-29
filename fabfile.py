from fabric.api import local, settings


def initial_setup():
    with settings(warn_only=True):
        local('docker network create radionica')


def build():
    local('git pull origin master')
    with settings(warn_only=True):
        local('docker stop seventweets-container')
        local('docker rmi seventweets-image')
    local('docker build -t seventweets-image .')


def start():
    local('docker run --rm -d --net radionica -p 5000:5000 --name seventweets-container seventweets-image')


def deployment():
    build()
    start()


def full_deployment():
    initial_setup()
    deployment()


def stop():
    local('docker stop seventweets-container')


def clear():
    local('docker stop seventweets-container')
    local('docker rmi seventweets-image')
