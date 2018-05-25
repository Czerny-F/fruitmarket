# fruitmarket

[![Build Status](https://travis-ci.org/Czerny-F/fruitmarket.svg?branch=master)](https://travis-ci.org/Czerny-F/fruitmarket)
[![Coverage Status](https://coveralls.io/repos/github/Czerny-F/fruitmarket/badge.svg?branch=master)](https://coveralls.io/github/Czerny-F/fruitmarket?branch=master)

fruit sales management

## Requirements
Tested with all combinations of:

- Python: 3.5, 3.6
- Django: 2.0

## Installation

```Console
$ git clone git@github.com:Czerny-F/fruitmarket.git
$ virtualenv venv
$ source venv/bin/activate
$ cd fruitmarket
$ pip install -r requirements.txt

$ python manage.py check
$ python manage.py test
$ python manage.py migrate
$ python manage.py createsuperuser
$ python manage.py compilemessages
$ python manage.py runserver_plus
```
