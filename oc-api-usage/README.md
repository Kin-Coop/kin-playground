# Open Collective API Usage Demo

Runs a script that does a few things with the OC API.

## Prerequisites

You will need:
* To set up a couple of Open Collective user accounts; 
* A token for each account;
* A host admin token.

To get a user token, follow the README of the neighbouring oc-auth project in this repo. You can reuse
the same web server to get different user tokens; you just need to be logged in as a different user each time.

For the admin token, you need to be made an admin of the working host account before generating a token. 
(The user and admin tokens can be the same.) 
Alternatively, ask [rjferrier](https://github.com/rjferrier) for an admin token for Kin Coop.


## Instructions

Below are instructions for running on Linux or Mac.


### 1. Create and populate an environment variable file

Open a terminal in the present directory and run:


```shell
cat > .env << EOF
USER_1_TOKEN=
USER_2_TOKEN=
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
