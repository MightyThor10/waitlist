################################
########### Waitlist ###########
############ README ############
################################

This is the code repository for Waitlist, developed by:
1. Andrew Allan
2. Ryan Gainor
3. Sean Lindell
4. Isaac Mast
5. Sayyed Hadi Razmjo
6. Annemarie Zheng
7. Stephen Hoag

Waitlist is tool meant to remedy the hassle that students
and professors are met with when course registration rolls
around. It provides a streamlined interface for professors
to list their classes and enable the waitlist when desired.
Students have a similarly streamlined interface where all
their waitlist needs are met.

################################
###### Technologies used: ######
################################

Web Framework: Django

Database: SQLite (TBD)

Other libraries:

Bootstrap

################################
########## References ##########
################################

First, make sure you are working with an up-to-date
version of the repository. Then, navigate to the base
directory of the waitlist repository:

### NOTE: 
the main branch may or may not run depending on the virtual env settings. We added a new library GDAL to our main branch that is giving us a hard time to fix. You may run studentview too for most of our UI functionalities. CI/CD for studentview branch runs fine. CI/CD fails because of GDAL for main. - update 4/11 12:39 PM. 

cd [PATH_TO_REPO]/waitlist

# To activate the virtual environment
source [ venv-var ]/bin/activate
# venv-var
MAC: .venv
PC: waitlist-env

# To start the django server
python3 Code/manage.py runserver


The command prompt should indicate where the development
server was started, which should match this address:

http://127.0.0.1:8000/

Open the address in a browser to view Waitlist.

More documentation under Artifacts folder.

