FROM python:3.10

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE llmine_core.settings

# create user for the Django project
RUN useradd -ms /bin/bash llmine_core

# set current user
USER llmine_core

# set work directory
WORKDIR /home/llmine_core

# copy and install pip requirements
COPY --chown=llmine_core ./requirements.txt /home/llmine_core/requirements.txt
ENV PATH /home/llmine_core/.local/bin:$PATH
RUN pip install --user -r /home/llmine_core/requirements.txt

# copy Django project files
COPY --chown=llmine_core . /home/llmine_core/

RUN ["chmod", "+x", "/home/llmine_core/docker-entrypoint-gunicorn.sh"]
RUN ["chmod", "+x", "/home/llmine_core/docker-entrypoint-celery.sh"]