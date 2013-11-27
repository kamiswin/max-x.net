#!/bin/bash
source /usr/local/bin/virtualenvwrapper.sh
workon pythoner

uwsgi --socket 127.0.0.1:8077 --chdir /root/maxfile/max-x.net/crawler -H /root/.virtualenvs/max-xn.com/ --module=crawler.wsgi --processes 4 --threads 2 --daemonize /root/maxfile/max-x.net/crawler/uwsgi.log