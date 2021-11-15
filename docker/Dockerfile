FROM python:3.8.9-slim

ENV MICRO_SERVICE=/synthesis
# set work directory


RUN mkdir -p $MICRO_SERVICE

# where the code lives
WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# The default user that should be used
ARG USER_ID=1000
ARG GROUP_ID=1000
ARG APP_USER=appuser

# Create user and group
RUN groupadd -g ${GROUP_ID} ${APP_USER} && useradd -u ${USER_ID} -g ${APP_USER} -s /bin/sh ${APP_USER}

# Install ca certificates
RUN apt-get update \
    && apt-get install ca-certificates python3-dev libpq-dev gcc -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip


COPY ./Pipfile $MICRO_SERVICE
COPY ./Pipfile.lock $MICRO_SERVICE

# install dependencies
RUN pip install --user pipenv
RUN python3 -m pipenv install

RUN chown -R ${APP_USER}:${APP_USER} /root
RUN chmod 755 /root

# copy project
COPY --chown=${APP_USER}:${APP_USER} . $MICRO_SERVICE

RUN mkdir -p $MICRO_SERVICE/app/staticfiles

# Set the default user
RUN chmod -R a+rwx $MICRO_SERVICE

USER ${APP_USER}


CMD ["/bin/bash", "-c", "/synthesis/docker/start_api.sh"]
