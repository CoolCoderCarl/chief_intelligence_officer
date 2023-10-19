# logger_image_tester

Custom container image for testing container env set up  
Simple python app which throw logs to stdout

It is possible to check network connectivity if pass config to application

## Prehistory
This program help to know when internet is available again and notify about it.

> I want my own "hello-world" image tester  
> (c) Author

Enjoy.

## How to use

You can check the last available tags here - `https://hub.docker.com/r/h0d0user/logger_image_tester`  

Or just download latest one - `docker pull h0d0user/logger_image_tester:latest`

From this moment this application kuberized, so you can just run it in your clusters as a DaemonSet
