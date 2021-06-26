#!/bin/bash

set -e

if [ -z "${RABBITAI_VERSION_RC}" ]; then
  echo "RABBITAI_VERSION_RC is required to run this container"
  exit 1
fi

if [ -z "${RABBITAI_SVN_DEV_PATH}" ]; then
  RABBITAI_SVN_DEV_PATH="$HOME/svn/rabbitai_dev"
fi

if [ ${1} == "local" ]; then
  RABBITAI_RELEASE_RC=apache-rabbitai-"${RABBITAI_VERSION_RC}"
  RABBITAI_RELEASE_RC_TARBALL="${RABBITAI_RELEASE_RC}"-source.tar.gz
  RABBITAI_TARBALL_PATH="${RABBITAI_SVN_DEV_PATH}"/${RABBITAI_VERSION_RC}/${RABBITAI_RELEASE_RC_TARBALL}
  RABBITAI_TMP_TARBALL_FILENAME=_tmp_"${RABBITAI_VERSION_RC}".tar.gz
  cp "${RABBITAI_TARBALL_PATH}" "${RABBITAI_TMP_TARBALL_FILENAME}"
  docker build --no-cache \
        -t apache-rabbitai:${RABBITAI_VERSION_RC} \
        -f Dockerfile.from_local_tarball . \
        --build-arg VERSION=${RABBITAI_VERSION_RC} \
        --build-arg RABBITAI_BUILD_FROM=local \
        --build-arg RABBITAI_RELEASE_RC_TARBALL="${RABBITAI_TMP_TARBALL_FILENAME}"
  rm "${RABBITAI_TMP_TARBALL_FILENAME}"
else
  # Building a docker from a tarball
  docker build --no-cache \
        -t apache-rabbitai:${RABBITAI_VERSION_RC} \
        -f Dockerfile.from_svn_tarball . \
        --build-arg VERSION=${RABBITAI_VERSION_RC} \
        --build-arg RABBITAI_BUILD_FROM=svn
fi

echo "---------------------------------------------------"
echo "After docker build and run, you should be able to access localhost:5001 on your browser"
echo "login using admin/admin"
echo "---------------------------------------------------"
if ! docker run -p 5001:8088 apache-rabbitai:${RABBITAI_VERSION_RC}; then
  echo "---------------------------------------------------"
  echo "[ERROR] Seems like this apache-rabbitai:${RABBITAI_VERSION_RC} has a setup/startup problem!"
  echo "---------------------------------------------------"
fi
