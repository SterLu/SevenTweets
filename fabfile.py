from fabric.api import run


def initial_setup():
    run('docker network create radionica')


def build():
    run('git pull origin master')
    run('docker rmi seventweets')
    run('docker build -t seventweets ./SevenTweets')


def start():
    run('docker run --rm -d --net radionica -p 5000:5000 seventweets')


def deployment():
    build()
    start()


def full_deployment():
    initial_setup()
    deployment()
