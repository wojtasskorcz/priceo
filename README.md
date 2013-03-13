priceo
======

Python/Django simple showcase web project


Table of Contents
=================

1. Installation.
2. Usage notes.
3. Python deployment manual for future use.

1. Installation.
----------------

The project was written using Python v. 2.7.3. There's no guarantee it'll work on any other version, although it doesn't use any advanced Python mechanics, so it should.

Create the folder in which you'll want to store your project, let's call it PROJECT_HOME. It has to be for this project only, as it will be bloated with files downloaded from the repository.

Enable version control (run in PROJECT_HOME)  
`git init`  
Download project files from the repository  
`git pull https://github.com/wojtasskorcz/priceo.git`  

When the files have been downloaded create a virtualenv in PROJECT_HOME.  
You'll need SetupTools for that so run in PROJECT_HOME  
`sudo easy_install -U SetupTools`  
And to install virtualenv run  
`python -m virtualenv --no-site-packages .`  
Switch to the local virtualenv context  
`source bin/activate`  
Install SetupTools in virtualenv  
`easy_install -U SetupTools`  
Install the required project dependencies  
`pip install -r requirements.txt`

Configure Eclipse to start developing the project.  
Run Eclipse, go to *Window -> Preferences -> PyDev -> Interpreter - Python -> New...*  
Select *PROJECT_HOME/bin/python* and give the interpreter any name you want. This is the local (the virtualenv one) interpreter, which has all the dependencies for the project.  
Click OK, don't change any libraries settings, ignore the error.  
With the new interpreter selected click New Folder and choose *PROJECT_HOME/bin*. Apply the changes.  
Import your the project into workspace. *RMB on the project folder -> Properties -> PyDev - Interpreter/Grammar* and choose the newly created interpreter.  
Go to *priceo.settings* and set the paths according to your local system, especially in *DATABASES, MEDIA_ROOT, STATICFILES_DIRS, TEMPLATE_DIRS*. Configuring the paths you should only change the part before "django-templates/priceo/" to point to the folder, where you put the "django-templates" folder downloaded from the repository. The rest of the path (after "django-templates/priceo/") should be left intact. As to the database, you're free to choose where you want to place it.  
*RMB on the project folder -> Django -> Sync DB*, create a new superuser  
*RMB on the project folder -> Run As -> PyDev: Django*  
Go to "localhost:8000" in your web browser to see, if the project works.  

2. Usage notes.
---------------

You should now have the project with an empty database up and running. You can either start adding records to the database going to "localhost:8000/admin/" in your web browser, or automatically fill the database with records predefined in the file *priceo.test*. To do that do the following  
*RMB on the project folder -> Django -> Shell with django environment*  
In the shell run the following commands  
`from priceo.test import test`  
`test()`  

The project is very minimalist in presentation and serves only as a showcase for the backend. Feel free to test all its features, propose new ones, improve the old ones and report bugs.

3. Python deployment manual for future use.
-------------------------------------------

When starting a new project configure it with virtualenv and appropriate Eclipse python interpreter, as described in the Installation section. This will make the project independend and unaware of the global python installation and libraries. It's the best way to avoid conflicts with other projects, the project is self-standing this way.

When developing an untracked project and wanting to upload it to GitHub (or any other repo) do the following.  
Create a new repo through the website, let's name it *test* here. Go to the project directory, let's call it PROJECT_HOME, and run the following:  
`git init`  
`git remote add --track master origin https://github.com/wojtasskorcz/test.git`  
`git add .`  
`git commit -a -m "initial import"`  
`git pull --rebase`  
Before pushing add to *.gitignore* all the files and patterns you don't want to upload. For Python with virtualenv it will certainly be all the virtualenv folders (they are useless on other machines due to broken symbolic links after upload), so the file might look like this:  
    *.log
    *.pot
    *.pyc
    local_settings.py
    bin
    include
    lib
    local
    sqlite.db
Also, copy any external resources, like django templates, to your project directory and add appropriate admonition in the readme as to where to put them after pulling.  
Create the file with required libraries by running in PROJECT_HOME (in context of virtualenv)  
`pip freeze > requirements.txt`  
This way the person that later pulls the project, will be able to follow the procedures of the first section of this readme (i.e. to run ``pip install -r requirements.txt``)  
Now you can safely push the project
`git push`  

