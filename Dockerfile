# using python 3.10 image
FROM python:3.10-slim

# set env
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# define in which folder we are going to store our application
# create new env var
ENV APP_HOME=/app
# create the folder for static files (create parent if missing)
RUN mkdir -p $APP_HOME/static
# declare the var which we define as the home of the app
# (just a fancy term for the folder where we are going to copy 
# your application from your laptop to the container[linus system])
WORKDIR $APP_HOME

# make the 8000 port of the container exposed to the laptop 8000 port
EXPOSE 8000
# copy the requirements file to which contains a
# all the necessary packages for your django application
# if you don't have this file and you already have your app working on a virtual environment then
# activate the virtual env and run this command 
# pip3 freeze > requirements.txt
# or pip if you don't have pip3

COPY requirements.txt $APP_HOME/requirements.txt
# then install these packages in the container
RUN pip install -r requirements.txt

# last step is to copy the whole application to the container
COPY . $APP_HOME
# === end ===
