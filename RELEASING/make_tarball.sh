#!/bin/bash

set -e

usage() {
   echo "usage: make_tarball.sh <RABBITAI_VERSION> <RABBITAI_RC> <PGP_KEY_FULLBANE>"
}

if [ -z "$1" ] || [ -z "$2" ] || [ -z "$3" ]; then
  if [ -z "${RABBITAI_VERSION}" ] || [ -z "${RABBITAI_RC}" ] || [ -z "${RABBITAI_PGP_FULLNAME}" ] || [ -z "${RABBITAI_RELEASE_RC_TARBALL}" ]; then
    echo "No parameters found and no required environment variables set"
    echo "usage: make_tarball.sh <RABBITAI_VERSION> <RABBITAI_RC> <PGP_KEY_FULLBANE>"
    usage;
    exit 1
  fi
else
  RABBITAI_VERSION="${1}"
  RABBITAI_RC="${2}"
  RABBITAI_PGP_FULLNAME="${3}"
  RABBITAI_RELEASE_RC_TARBALL="apache-rabbitai-${RABBITAI_VERSION_RC}-source.tar.gz"
fi

RABBITAI_VERSION_RC="${RABBITAI_VERSION}rc${RABBITAI_RC}"

if [ -z "${RABBITAI_SVN_DEV_PATH}" ]; then
  RABBITAI_SVN_DEV_PATH="$HOME/svn/rabbitai_dev"
fi

if [[ ! -d "${RABBITAI_SVN_DEV_PATH}" ]]; then
  echo "${RABBITAI_SVN_DEV_PATH} does not exist, you need to: svn checkout"
  exit 1
fi

if [ -d "${RABBITAI_SVN_DEV_PATH}/${RABBITAI_VERSION_RC}" ]; then
  echo "${RABBITAI_VERSION_RC} Already exists on svn, refusing to overwrite"
  exit 1
fi

RABBITAI_RELEASE_RC_TARBALL_PATH="${RABBITAI_SVN_DEV_PATH}"/"${RABBITAI_VERSION_RC}"/"${RABBITAI_RELEASE_RC_TARBALL}"
DOCKER_SVN_PATH="/docker_svn"

# Building docker that will produce a tarball
docker build -t apache-builder -f Dockerfile.make_tarball .

# Running docker to produce a tarball
docker run \
      -e RABBITAI_SVN_DEV_PATH="${DOCKER_SVN_PATH}" \
      -e RABBITAI_VERSION="${RABBITAI_VERSION}" \
      -e RABBITAI_VERSION_RC="${RABBITAI_VERSION_RC}" \
      -e HOST_UID=${UID} \
      -v "${RABBITAI_SVN_DEV_PATH}":"${DOCKER_SVN_PATH}":rw \
      -ti apache-builder

gpg --armor --local-user "${RABBITAI_PGP_FULLNAME}" --output "${RABBITAI_RELEASE_RC_TARBALL_PATH}".asc --detach-sig "${RABBITAI_RELEASE_RC_TARBALL_PATH}"
gpg --print-md --local-user "${RABBITAI_PGP_FULLNAME}" SHA512 "${RABBITAI_RELEASE_RC_TARBALL_PATH}" > "${RABBITAI_RELEASE_RC_TARBALL_PATH}".sha512

echo ---------------------------------------
echo Release candidate tarball is ready
echo ---------------------------------------
