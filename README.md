# Django Vue SSR Playground

This repo is a how-to server render a Vue App using Django.

## Installation
This project runs under ```python```, so you need to have installed ```virtualenv``` to isolate the dependencies. To build frontend and run render server you should have installed ```NodeJS``` and ```npm```.

```bash
$ git clone https://github.com/marcopuccio/django-vue-ssr-playground
$ cd django-vue-ssr-playground
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ npm install
```

## Run
Open your term and start the python server.
```bash
$ source env/bin/activate
$ python manage.py runserver
```
Then, open other term and init dev server with npm and webpack
```bash
$ npm start
```
After all, navigate to ```http://localhost:8080```.
