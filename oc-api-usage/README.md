# Open Collective API Usage Demo

Runs a script that does a few things with the OC API.

## Prerequisites

You will need:
* User token
* Admin token

To get a user token, follow the README of the neighbouring oc-auth project in this repo.

For the admin token (Item 4), you need to be made an admin of the working host account
before generating a token. (The user and admin tokens can be the same.)
Alternatively, ask [rjferrier](https://github.com/rjferrier) to generate an admin token.


## Instructions

Below are instructions for running on Linux or Mac.


### 1. Create and populate an environment variable file

Open a terminal in the present directory and run:


```shell
cat > .env << EOF
USER_TOKEN=
ADMIN_TOKEN=
EOF
```

Paste the user and admin tokens into this file.


### 2. Run the app

Create a virtual env, install libraries, set environment variables and run the script. 
To do this, open a terminal and run:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export $(cat .env | xargs)
python oc_api_usage.py
```
