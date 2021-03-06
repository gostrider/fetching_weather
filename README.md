## A toy project for fetching weather data from `openweathermap.org`

Description:

This project built with Tornado web server for fetching data from `openweathermap.org` and persist into `couchbase`.


Challenge:

The web server part was originally intended to be dockerize as well.
However, it will cost longer time to figure out installing libcouchbase for python couchbase client in the docker image.
Therefore, this version is only contain the web application source code and a startup script for running dockerized couchbase.

### Project Requirement:
 - Python version: 3.6.0
 - Web Server: Tornado, version: 4.4.2
 - Storage: (Docker container) Couchbase

### Installation:

Install python 3.6+

Tornado: `pip install tornado`

couchbase client: `pip install couchbase`

libcouchbase for python client: https://developer.couchbase.com/server/other-products/release-notes-archives/c-sdk


### To Run this project:  `./run.sh`