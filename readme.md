# Bitcoin Notification Service

This is a web application that receives a 
* Valid Bitcoin transaction hash, 
* confirmations 
* trigger url 

It checks to see if the specified transaction has met the confirmation level then triggers the url.

For example a transcation 
### Install components
* Redis ( ensure redis is running )
* Python 3.x ( x >= 4 )

### Requirements

```bash
$ pip install -r requirements.txt
```

### Architecture

- - - - -  - - - - - -       -- - - - - - - - -
| user query endpoint |  ->  | redis pub n sub |
- - - -- - - - - - - -       - - - - - - - - -

#### Celery Asynchronous tasks

The background workers are managed using celery

 - - - - -  - -
| subscriber  |  -> trigger hooks ->
------ -- - - -
### Configuration

```bash
cp .env.example .env
```

Fill in the details for the following
```
RPC_HOST=xxxx
RPC_PORT=xxx
RPC_USER=xxxxx
RPC_PASSWORD=xxxxxxxx
ZERO_MQ_HOST=xxx
ZERO_MQ_PORT=xxxx
```

### Run Tests
```sh
pytest tests/
```

### Run Server
To run the python server
```sh
python server.py
```
You should see the below output the port is based on what's specified in the env file

```
Accepting connections on http://0.0.0.0:8082
```

### Server deployment

The background processes are managed using supervisord.
The supervisor conf file can be found in `scripts\bns-service.conf`

Make the startup script executable by running

```bash
sudo chmod a+x ./startup.sh
```

Set the base path for the logs
```
export BNS_LOGPATH=/var/log/bns-service
```
Then run the below command:

```bash
./startup.sh
```

### Contributor
@samparsky



