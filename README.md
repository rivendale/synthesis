# [Synthesis](https://synthesis.page)

This is an analytics site to check if a user owns an NFT in one of the major NFT clubs such as [Rumble Kong League](https://www.rumblekongleague.com/) or [Bored Ape Yacht](https://boredapeyachtclub.com/).

---
## Api Documentation

- use this [link](/api/v1/graphql/) to access the api documentation

> ## How to set up the project.

### Features.

- python 3.9
- postgreSQL as database engine
- pipenv

---

### PROJECT SETUP.

- clone the repository

```
$ https://github.com/rivendale/synthesis.git
```

- cd into the directory

```
$ cd ~/De/P/Upwork/ethsigns/synthesis
```

### create environment variables
  On Unix or MacOS, run:

```
$ cp .env.example .env
```

You can edit whatever values you like in there.

Note: There is no space next to '='
##### On terminal,

```
$ source .env
```
---

<center>OPTION 1 (Manual setup)</center>

> > ##### VIRTUAL ENVIRONMENT

---

**To Create:**

`make env`

---

**To Activate:**

`make activate`

---

**Installing dependencies:**

`make install`


> > ### MIGRATIONS - DATABASE

---

**Make migrations**

`make makemigrations`

---

**Update DB with the latest migrations**

`make migrate`

---

> > ### THE APPLICATION

---

**run application**

`make run`

---

**run linter**

`make lint`

---

**run tests**

## `make test`

> > ### SAVING WORK TO GIT

---

`git add .`

`git commit -m "comment"`

`git push origin main`

---

<center>OPTION 2 (Set Up Development With Docker)</center>

---

1. Download Docker from [here](https://docs.docker.com/)
2. Set up an account to download Docker
3. Install Docker after download
4. Go to your terminal run the command `docker login`
5. Input your Docker email and password

To setup for development with Docker after cloning the repository please do/run the following commands in the order stated below:

- `cd <project dir>` to checkout into the dir
- `docker-compose build` or `make build` to build the application images
- `docker-compose up -d` or `make start` or `make start-verbose` to start the api after the previous command is successful

The `docker-compose build` or `make build` command builds the docker image where the api and its postgres database would be situated.
Also this command does the necessary setup that is needed for the API to connect to the database.

The `docker-compose up -d` or `make start` command starts the application while ensuring that the postgres database is seeded before the api starts.

The `make start-verbose` command starts the api verbosely to show processes as the container spins up providing for the visualization of errors that may arise.

To stop the running containers run the command `docker-compose down` or `make stop`

**To Clean Up After using docker do the following**

1. In the project directory, run the command `bash cleanup.sh` or `make clean`
2. Wait for all images to be deleted.

**URGENT WARNING** PLEASE DO NOT RUN THE CLEAN-UP COMMAND ABOVE UNLESS YOU ARE ABSOLUTELY SURE YOU ARE DONE WITH THAT DEVELOPMENT SESSION AND HAVE NO DATA THAT WOULD BE LOST IF CLEAN-UP IS DONE!

**Alternative cleanup method**

Instead of using the above command, you can delete images with the command `docker rmi repository:tag`

You can can run the command `docker images` to see the image **repository:tag** you may want to delete

---

---

**Running Redis server**

- You can install redis by running the command `bash redis.sh` in the root project directory, this will install redis for you (if not already installed) and also run/start the redis server for the first time on your local machine.

**Running Celery worker**
Please endevour to update the `.env` file with the following keys and the appropriate values(`redis_server_url`):
` export CELERY_BROKER_URL=<Your_Redis_Server_URL> `

---

- To run redis after it has been stopped run `redis-server`

- In a new terminal tab run the Celery Message Worker with:

  ```
    make celery_worker
  ```
- In a new terminal tab run the Celery Beat with:

  ```
    make celery_beat
  ```
---
---

## API documentation

> For the API documentation, Go to insomnia and import `Insomnia.json` located in the project base directory

> The API url is:

```
{base-url}/api/v1/graphql/
```

---
