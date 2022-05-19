######################################################################
# PY 阶段，简单地使用 pip 安装必须的软件包
######################################################################
ARG PY_VER=3.7.9
FROM python:${PY_VER} AS rabbitai-py

# 在安装Python软件包前，创建应用程序根目录，安装系统支撑软件
RUN mkdir /app \
        && apt-get update -y \
        && apt-get install -y --no-install-recommends \
            build-essential \
            default-libmysqlclient-dev \
            libpq-dev \
            libsasl2-dev \
            libecpg-dev \
        && rm -rf /var/lib/apt/lists/*

# 首先，我们安装必须的软件包，允许我们利用缓存，以便当且仅当需求发生变化时构建
COPY ./requirements/*.txt  /app/requirements/
COPY setup.py MANIFEST.in README.md /app/
COPY rabbitai-frontend/package.json /app/rabbitai-frontend/
RUN cd /app \
    && mkdir -p rabbitai/static \
    && touch rabbitai/static/version_info.json \
    && pip install --no-cache -r requirements/local.txt


######################################################################
# Node 阶段，处理静态资源的构建
######################################################################
FROM node:14 AS rabbitai-node

ARG NPM_VER=7
RUN npm install -g npm@${NPM_VER}

ARG NPM_BUILD_CMD="build"
ENV BUILD_CMD=${NPM_BUILD_CMD}

# 首先使用 npm ci 安装依赖软件
RUN mkdir -p /app/rabbitai-frontend
RUN mkdir -p /app/rabbitai/static/assets
COPY ./docker/frontend-mem-nag.sh /
COPY ./rabbitai-frontend/package* /app/rabbitai-frontend/
RUN /frontend-mem-nag.sh \
        && cd /app/rabbitai-frontend \
        && npm ci

# 接下来，复制剩余的内容以便 webpack 完成相关工作
COPY ./rabbitai-frontend /app/rabbitai-frontend
RUN cd /app/rabbitai-frontend \
        && npm run ${BUILD_CMD} \
        && rm -rf node_modules


######################################################################
# 最终瘦身镜像 ...
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

RUN mkdir -p ${PYTHONPATH} \
        && useradd --user-group -d ${RABBITAI_HOME} -m --no-log-init --shell /bin/bash rabbitai \
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

## 最后，让我们安装 rabbitai
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
