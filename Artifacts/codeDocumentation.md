# See README for instructions on installation and running the django server

## What a user can do with our prototype

Our first prototype delivered key functionalities such as student login, signup, viewing courses. We have
expanded the functionality to support professors moving students' positions on the waitlist. Our prototype
supports accepting or rejecting students onto waitlists, and for professors to change the details of the
waitlists they own using advanced features. They can also choose to make their waitlist anonymous or not and sort students based on 
different algorithms. We have also made some changes to the UI to make it more appealing to the users. Please download and run our project locally or test it live on the pythonanywhere link given in the main readme. 

## To run unit tests

1. python3 [Code]/manage.py test [Code]/users
2. python3 [Code]/manage.py test [Code]/studentview

## Tutorial Information

Tutorial utilized: [https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)

Notes: the blog he mentions in the video is synonymous to the studentview application

## File Documentation:

- Code
- Django_setup-folder
  - Urls.py: contains urlpatterns to get to specific [insertappname].urls
- Studentview-folder: manages the application for the student part of waitlist
  - Migrations-folder: auto-generated
  - Static-folder
    - studentview-folder
      - Main.css: contains specs for styles of different items
  - Templates-folder
    - studentview-folder
      - Base.html: contains the base html data that will be inherited by other html.
      - Home.html: override block content to show classes 
      - Join_waitlist.html: override block content to show joining the waitlist
  - Views.py: contains functions to render home and joinWaitlist pages and some hardcoded data for testing
  - Urls.py: contains part of path to indicate which path to use and what function under views is used 
- Other files: have not been touched auto-generated

## How the website URL data is found in the code logic:

1. The website URL: `http://localhost:8000/studenthome/joinwaitlist/`
2. We get `studenthome/joinwaitlist/`
3. Looks at `django_setup urls.py urlpatterns` and sees it has `path('studenthome/', include('studentview.urls'))` which matches the first extension.
4. It then chops off `studenthome/` and then passes `joinwaitlist/` to `studentview urls.py` which also matches url patterns and returns `views.joinWaitlist`.

## How to create a superuser to access http://localhost:8000/admin/:

1. Navigate to where `manage.py` is located
2. On command line type: `python manage.py createsuperuser`
3. Follow prompts below
4. Run server and go to `http://localhost:8000/admin/` then login

## Information on Authentication in Django:

[https://docs.djangoproject.com/en/4.2/topics/auth/default/](https://docs.djangoproject.com/en/4.2/topics/auth/default/)
