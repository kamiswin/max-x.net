#!/bin/bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo $DIR


SPIDER_PATH="$DIR/../seraph_spider"
COM_PATH="$DIR/../.."
NEW_COM=$(cd $COM_PATH;pwd)

echo $NEW_COM

source /usr/local/bin/virtualenvwrapper.sh
workon max-xn.com

export PYTHONPATH=$NEW_COM:$PYTHONPATH


cd $NEW_COM
kill -9 `pgrep -f autohome.py`
kill -9 `pgrep -f chinaluxus.py`
kill -9 `pgrep -f new527motor.py`
kill -9 `pgrep -f neeu.py`
python $SPIDER_PATH/autohome.py
python $SPIDER_PATH/chinaluxus.py
python $SPIDER_PATH/new527motor.py
python $SPIDER_PATH/neeu.py
python $SPIDER_PATH/autohome_fix.py