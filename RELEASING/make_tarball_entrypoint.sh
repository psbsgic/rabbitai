#!/bin/bash

set -e

if [ -z "${RABBITAI_VERSION_RC}" ] || [ -z "${RABBITAI_SVN_DEV_PATH}" ] || [ -z "${RABBITAI_VERSION}" ]; then
  echo "RABBITAI_VERSION_RC, RABBITAI_SVN_DEV_PATH and RABBITAI_VERSION are required to run this container"
  exit 1
fi

RABBITAI_RELEASE_RC=apache-rabbitai-"${RABBITAI_VERSION_RC}"
RABBITAI_RELEASE_RC_TARBALL="${RABBITAI_RELEASE_RC}"-source.tar.gz
RABBITAI_RELEASE_RC_BASE_PATH="${RABBITAI_SVN_DEV_PATH}"/"${RABBITAI_VERSION_RC}"
RABBITAI_RELEASE_RC_TARBALL_PATH="${RABBITAI_RELEASE_RC_BASE_PATH}"/"${RABBITAI_RELEASE_RC_TARBALL}"

# Create directory release version
mkdir -p "${RABBITAI_SVN_DEV_PATH}"/"${RABBITAI_VERSION_RC}"

# Clone rabbitai from tag to /tmp
cd /tmp
git clone --depth 1 --branch ${RABBITAI_VERSION_RC} https://github.com/apache/rabbitai.git
mkdir -p "${HOME}/${RABBITAI_VERSION_RC}"
cd rabbitai && \

# Check RC version
if ! jq -e --arg RABBITAI_VERSION $RABBITAI_VERSION '.version == $RABBITAI_VERSION' rabbitai-frontend/package.json
then
  SOURCE_VERSION=$(jq '.version' rabbitai-frontend/package.json)
  echo "Source package.json version is wrong, found: ${SOURCE_VERSION} should be: ${RABBITAI_VERSION}"
  exit 1
fi

# Create source tarball
git archive \
    --format=tar.gz "${RABBITAI_VERSION_RC}" \
    --prefix="${RABBITAI_RELEASE_RC}/" \
    -o "${RABBITAI_RELEASE_RC_TARBALL_PATH}"

chown -R ${HOST_UID}:${HOST_UID} "${RABBITAI_RELEASE_RC_BASE_PATH}"
