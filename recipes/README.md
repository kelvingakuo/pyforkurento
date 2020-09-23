A set of Django recipes to test pyforkurento and Kurento Media Server

## Pre-requisites
1. [Install Docker](https://docs.docker.com/engine/install/)
2. [Install Kurento Media Server](https://hub.docker.com/r/kurento/kurento-media-server)
3. Run Kurento Media Server (If it's running on a port other than 8888, change the port inside consumers.py)
```docker run -d --name kms --network host kurento/kurento-media-server:latest```
4. Install [pyforkurento](https://pyforkurento.readthedocs.io/en/latest/), preferably in a [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
5. Install Django and channels, preferably in the same Virtualenv
```pip install -r requirements.txt```

## Usage
In each directory, you'll find a dir named _static_ , and ```manage.py``` at the same level.
1. Find the ```html``` file inside ```static/``` then open it in a browser
2. Do ```python manage.py runserver```. If the port is not 8000, change it in the ```html`` file