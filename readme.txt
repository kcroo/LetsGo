INITIAL SETUP 

- set up virtual environment on flip, in folder of your choice 
bash 
virtualenv venv -p $(which python3)
source ./venv/bin/activate

- upgrade pip3 and install packages 
pip3 install --upgrade pip
pip3 install -r requirements.txt                # does this work? might need to change this 


RUN SERVER ON FLIP (WITH DEBUG)

- do this if you're not in virtual environment 
bash 
source ./venv/bin/activate
export FLASK_APP=run.py
export FLASK_DEBUG=1						
python -m flask run -h 0.0.0.0 -p 5473

- run server persistently (replace #### with port number)
gunicorn run:app -b 0.0.0.0:#### -D

- log in to VPN to see website 
ex: http://flip2.engr.oregonstate.edu:5472/ 
    where 5472 is port number 


RESET DATABASE (with dummy data)

- log in to mysql
mysql -u cs340_corraok -p -h classmysql.engr.oregonstate.edu cs340_corraok

- source travelplanner/static/databaseSetup.sql


POSSIBLE ISSUES 

- need hard reset after changing static file 
in browser, ctrl-shift-r
