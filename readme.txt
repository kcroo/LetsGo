INITIAL SETUP 

- set up virtual environment on flip, in folder of your choice 
bash 
virtualenv venv -p $(which python3)
source ./venv/bin/activate

- upgrade pip3 and install packages 
pip3 install --upgrade pip
pip3 install -r requirements.txt


RUN SERVER ON FLIP (WITH DEBUG)

- do this if you're not in virtual environment 
bash 
source ./venv/bin/activate

- export app and run server (replace #### with port number)
export FLASK_APP=app.py
export FLASK_DEBUG=1						
python -m flask run -h 0.0.0.0 -p 5472	

- run server persistently (replace #### with port number)
gunicorn run:app -b 0.0.0.0:#### -D

- log in to VPN to see website 
ex: http://flip2.engr.oregonstate.edu:5472/ 
    where 5472 is port number 


POSSIBLE ISSUES 

- need hard rest after changing static file 
in browser, ctrl-shift-r