#!/bin/bash

case $1 in
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

    start)
        cd server && source venv/bin/activate && (python api.py &) && cd .. && cd client && (npm start &) && cd ..
    ;;

    checkport)
        sudo lsof -i :$2
    ;;
esac