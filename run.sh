#!/bin/bash

source venv/bin/activate
python server/api.py

cd client && npm start