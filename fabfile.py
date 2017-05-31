from fabric.api import local, settings


def full_deploy(db_user, db_pw):
    initial_setup(db_user, db_pw)
    deploy(db_user, db_pw)
    bootstrap_storage()


def initial_setup(db_user, db_pw):
    with settings(warn_only=True):
        local('docker network create radionica')
        local('docker volume create radionica-postgres-data')
        start_storage(db_user, db_pw)


def start_storage(db_user, db_pw):
    with settings(warn_only=True):
        local('docker stop storage-container')
    local('docker run --rm -d --name storage-container --net radionica -p 127.0.0.1:5432:5432 \
           -e POSTGRES_USER={db_user} -e POSTGRES_PASSWORD={db_pw} \
           -v radionica-postgres-data:/var/lib/postgresql/data postgres:9.6.2'
          .format(db_user=db_user, db_pw=db_pw))


def deploy(db_user, db_pw):
    build()
    start(db_user, db_pw)


def update():
    local('git pull origin master')


def build():
    update()
    with settings(warn_only=True):
        local('docker stop seventweets-container')
        local('docker rmi seventweets-image')
    local('docker build -t seventweets-image .')


def start(db_user, db_pw):
    local('docker run --rm -d --name seventweets-container --net radionica -p 8000:8000 \
           -e POSTGRES_USER={db_user} -e POSTGRES_PASS={db_pw} seventweets-image'
          .format(db_user=db_user, db_pw=db_pw))


def bootstrap_storage():
    local('docker exec -it seventweets-container python -m seventweets storage')


def add_api_key(key):
    local('docker exec -it seventweets-container python -m seventweets storage {key}'
          .format(key=key))


def stop():
    local('docker stop seventweets-container')


def clear():
    local('docker rmi seventweets-image')
    local('docker stop seventweets-container')
