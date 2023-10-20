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

## Environment variables

In K8S manifest you can use some vars to configure network testing

```     
- name: SETTINGS_FILE_FOR_DYNACONF
  value: "/mnt/settings.toml"
- name: IS_IPV6
  value: "True"
- name: VERBOSE
  value: "True"
```

1) `SETTINGS_FILE_FOR_DYNACONF` - is a predefined var of dynaconf where it will be search for conf file
2) `IS_IPV6` - is a switcher needed when targeted networks has IPv6 addresses
3) `VERBOSE` - is a switcher needed when you want more results 