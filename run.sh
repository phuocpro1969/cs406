#!/bin/bash

case $1 in
    be)
        cd server
        source venv/bin/activate
        python api.py
    ;;

    fe)
        cd client
        npm start
    ;;

    push)
        if [ -z "$2" ]; then
            commit="update code"
            else
            commit=$2
        fi

        git add .
        git commit -m "$commit"
        git push
    ;;
esac