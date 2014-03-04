#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
export PYTHONPATH=$DIR:$PYTHONPATH
export ENV=$1
source /usr/local/bin/virtualenvwrapper.sh
workon max-xn.com

uwsgi --socket 127.0.0.1:8077 --chdir /root/Projects/max-x.net/crawler -H /root/.virtualenvs/max-xn.com/ --module=crawler.wsgi --processes 4 --threads 2 --daemonize /root/Projects/max-x.net/crawler/uwsgi.log