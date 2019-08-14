This app is written in Python Flask framework. Getting it running requires Python 3, pip, and virtualenv.

If you don't have pip and virtualenv installed, run:

    sudo easy_install pip
    sudo pip install virtualenv

Then, cd to this directory and create a virtualenv:

    virtualenv .virtualenv

Then, active your virtualenv:

    source .virtualenv/bin/activate

Now, you can install the project's dependencies:

    pip install -r requirements.txt

And start up the server with:
    (I use Mac OS)
    python3 main.py

Set the port to 5000 in the code, so this url should run:
http://127.0.0.1:5000/

To end the process:
    Control+C 