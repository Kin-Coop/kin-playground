# Open Collective API Auth Token Fetcher

Fetches a bearer token from OC's OAuth server so that you can put it in an Authorization header 
and start making requests to their API. 
Refer to [their docs](https://docs.opencollective.com/help/developers/oauth) for more info.


## Instructions

Below are instructions for running on Linux or Mac.

### 1. Create an environment variable file

Open a terminal in the present directory and run:

```shell
cat > .env << EOF
DOMAIN=
OC_CLIENT_ID=
OC_CLIENT_SECRET=
EOF
```

### 1. Set up ngrok

ngrok facilitates redirects between Open Collective and the locally running app
by creating a tunnel between the internet and the localhost port the app is exposed on.

1. Go to https://ngrok.com/ and create an account.
2. Follow the instructions to download and install ngrok and add your auth token to the 
   ngrok config.
3. Claim a free static domain. Click the menu in the top left corner of the ngrok 
   website. Go to Cloud Edge > Domains and claim a domain.
4. Copy the ngrok domain string ending in `.ngrok-free.app` and paste it into your 
   .env file so that it reads:

```
DOMAIN=<YOUR NGROK DOMAIN>
```


### 2. Set up an Open Collective client app

1. Go to https://opencollective.com and create an account.
2. On the dashboard, go to Settings > For developers and click `Create OAuth app`.
3. Set a name for the app, and set the callback URL as `https://<YOUR NGROK DOMAIN>/token`.
4. Copy the client ID and secret from the success page into the .env file:

```
OC_CLIENT_ID=<YOUR CLIENT ID>
OC_CLIENT_SECRET=<YOUR CLIENT SECRET>
```


### 3. Run the app

1. Install Python 3, if it isn't installed already.
2. Create a virtual env, install libraries, set environment variables and run the script. 
   To do this, open a terminal and run:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export $(cat .env | xargs)
python oc_auth.py
```

### 4. Run ngrok

Open another terminal and run:

```shell
export $(cat .env | xargs)
ngrok http --domain=$DOMAIN 8080
```

### 5. Get a token

1. In a browser, navigate to `localhost:8080` or `<YOUR NGROK DOMAIN>`.
2. Click "Get a token", and click the Authorize button when directed.
3. The resulting string is the bearer token and can be used in further API calls with the 
   auth header:

```
Authorization: Bearer <YOUR BEARER TOKEN>
```