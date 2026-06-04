#!/bin/bash


# install dependencies (if you haven’t already)
python3 -m pip install -r requirements.txt

# using the Flask CLI
export FLASK_APP=app.py          # macOS / Linux
# (on Windows PowerShell: setx FLASK_APP app.py)
flask run

# OR simply:
python3 app.py                  # runs with debug=True