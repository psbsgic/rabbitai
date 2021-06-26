######################################################################
# PY stage that simply does a pip install on our requirements
######################################################################
ARG PY_VER=3.7.9
FROM python:${PY_VER} AS rabbitai-py

RUN mkdir /app \
        && apt-get update -y \
        && apt-get install -y --no-install-recommends \
            build-essential \
            default-libmysqlclient-dev \
            libpq-dev \
            libsasl2-dev \
            libecpg-dev \
        && rm -rf /var/lib/apt/lists/*

# First, we just wanna install requirements, which will allow us to utilize the cache
# in order to only build if and only if requirements change
COPY ./requirements/*.txt  /app/requirements/
COPY setup.py MANIFEST.in README.md /app/
COPY rabbitai-frontend/package.json /app/rabbitai-frontend/
RUN cd /app \
    && mkdir -p rabbitai/static \
    && touch rabbitai/static/version_info.json \
    && pip install --no-cache -r requirements/local.txt


######################################################################
# Node stage to deal with static asset construction
######################################################################
FROM node:14 AS rabbitai-node

ARG NPM_VER=7
RUN npm install -g npm@${NPM_VER}

ARG NPM_BUILD_CMD="build"
ENV BUILD_CMD=${NPM_BUILD_CMD}

# NPM ci first, as to NOT invalidate previous steps except for when package.json changes
RUN mkdir -p /app/rabbitai-frontend
RUN mkdir -p /app/rabbitai/assets
COPY ./docker/frontend-mem-nag.sh /
COPY ./rabbitai-frontend/package* /app/rabbitai-frontend/
RUN /frontend-mem-nag.sh \
        && cd /app/rabbitai-frontend \
        && npm ci

# Next, copy in the rest and let webpack do its thing
COPY ./rabbitai-frontend /app/rabbitai-frontend
# This is BY FAR the most expensive step (thanks Terser!)
RUN cd /app/rabbitai-frontend \
        && npm run ${BUILD_CMD} \
        && rm -rf node_modules


######################################################################
# Final lean image...
######################################################################
ARG PY_VER=3.7.9
FROM python:${PY_VER} AS lean

ENV LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    FLASK_ENV=production \
    FLASK_APP="rabbitai.app:create_app()" \
    PYTHONPATH="/app/pythonpath" \
    RABBITAI_HOME="/app/rabbitai_home" \
    RABBITAI_PORT=8088

RUN useradd --user-group -d ${RABBITAI_HOME} --no-log-init --shell /bin/bash rabbitai \
        && mkdir -p ${PYTHONPATH} \
        && apt-get update -y \
        && apt-get install -y --no-install-recommends \
            build-essential \
            default-libmysqlclient-dev \
            libsasl2-modules-gssapi-mit \
            libpq-dev \
        && rm -rf /var/lib/apt/lists/*

COPY --from=rabbitai-py /usr/local/lib/python3.7/site-packages/ /usr/local/lib/python3.7/site-packages/
# Copying site-packages doesn't move the CLIs, so let's copy them one by one
COPY --from=rabbitai-py /usr/local/bin/gunicorn /usr/local/bin/celery /usr/local/bin/flask /usr/bin/
COPY --from=rabbitai-node /app/rabbitai/static/assets /app/rabbitai/static/assets
COPY --from=rabbitai-node /app/rabbitai-frontend /app/rabbitai-frontend

## Lastly, let's install rabbitai itself
COPY rabbitai /app/rabbitai
COPY setup.py MANIFEST.in README.md /app/
RUN cd /app \
        && chown -R rabbitai:rabbitai * \
        && pip install -e .

COPY ./docker/docker-entrypoint.sh /usr/bin/

WORKDIR /app

USER rabbitai

HEALTHCHECK CMD curl -f "http://localhost:$RABBITAI_PORT/health"

EXPOSE ${RABBITAI_PORT}

ENTRYPOINT ["/usr/bin/docker-entrypoint.sh"]

######################################################################
# Dev image...
######################################################################
FROM lean AS dev
ARG GECKODRIVER_VERSION=v0.28.0
ARG FIREFOX_VERSION=88.0

COPY ./requirements/*.txt ./docker/requirements-*.txt/ /app/requirements/

USER root

RUN apt-get update -y \
    && apt-get install -y --no-install-recommends libnss3 libdbus-glib-1-2 libgtk-3-0 libx11-xcb1

# Install GeckoDriver WebDriver
RUN wget https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz -O /tmp/geckodriver.tar.gz && \
    tar xvfz /tmp/geckodriver.tar.gz -C /tmp && \
    mv /tmp/geckodriver /usr/local/bin/geckodriver && \
    rm /tmp/geckodriver.tar.gz

# Install Firefox
RUN wget https://download-installer.cdn.mozilla.net/pub/firefox/releases/${FIREFOX_VERSION}/linux-x86_64/en-US/firefox-${FIREFOX_VERSION}.tar.bz2 -O /opt/firefox.tar.bz2 && \
    tar xvf /opt/firefox.tar.bz2 -C /opt && \
    ln -s /opt/firefox/firefox /usr/local/bin/firefox

# Cache everything for dev purposes...
RUN cd /app \
    && pip install --no-cache -r requirements/docker.txt \
    && pip install --no-cache -r requirements/requirements-local.txt || true
USER rabbitai


######################################################################
# CI image...
######################################################################
FROM lean AS ci

COPY --chown=rabbitai ./docker/docker-bootstrap.sh /app/docker/
COPY --chown=rabbitai ./docker/docker-init.sh /app/docker/
COPY --chown=rabbitai ./docker/docker-ci.sh /app/docker/

RUN chmod a+x /app/docker/*.sh

CMD /app/docker/docker-ci.sh
