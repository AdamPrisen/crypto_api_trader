# Cryptocurrency API

This API is used for trading with cryptocurrencies.

## Extensions
* flask
* flask-restful
* marshmallow 
* sqlalchemy 
* marshmallow-sqlalchemy 
* flask-marshmallow
* python-dotenv
* flask-sqlalchemy

Python vesrion: 3.8

## Installation

Use  [pipenv](https://github.com/pypa/pipenv) to install all requirments

```bash
pipenv install
pipenv shell
```
Or install all extensions according to[requirements.txt](requirements.txt)

## Configuration
1. **Required:** make your own **.env** file according to [.env.example](.env.example)
2. **Optional:** In [default_config.py](default_config.py) set your develop settings
3. **Optional:** In [config.py](config.py) set your production settings

## Run App
```bash
python app.py
```

## Run tests
```bash
python tests.py
```

## Usage
Examples of usage you can find in [documentation](https://documenter.getpostman.com/view/11352173/T17CDAGw?version=latest)