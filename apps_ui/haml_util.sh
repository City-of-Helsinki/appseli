#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SRC_DIR=$DIR/src
STATIC_DIR=$DIR/static/apps_ui
TEMPLATE_DIR=$DIR/templates/apps_ui

function compile {
    serve export $SRC_DIR $STATIC_DIR
    mkdir -p $STATIC_DIR/stylesheets
    lessc $SRC_DIR/stylesheets/screen.less > $STATIC_DIR/stylesheets/screen.css
    mv $STATIC_DIR/index.html $TEMPLATE_DIR/index.html
}

if [ "$1" == "compile" ]; then
    echo "Compiling"
    compile
elif [ "$1" == "watch" ]; then
    echo "Watching for changes"
    last_checksum=""
    while true; do
        checksum="`ls -lR $SRC_DIR | md5`"
        if [ "$checksum" != "$last_checksum" ]; then
            echo "Change detected"
            compile
            last_checksum="$checksum"
        fi
        sleep 1
    done
else
    echo "Usage: $0 [ compile | watch ]"
    echo "Requirements: serve, lessc"
fi
