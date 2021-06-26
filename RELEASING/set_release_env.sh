#!/bin/bash

usage() {
   echo "usage (BASH): . set_release_env.sh <RABBITAI_RC_VERSION> <PGP_KEY_FULLNAME>"
   echo "usage (ZSH): source set_release_env.sh <RABBITAI_RC_VERSION> <PGP_KEY_FULLNAME>"
   echo
   echo "example: source set_release_env.sh 0.37.0rc1 myid@apache.org"
}

if [ -z "$1" ] || [ -z "$2" ]; then
  usage;
else
  if [[ ${1} =~ ^([0-9]+)\.([0-9]+)\.([0-9]+)rc([0-9]+)$ ]]; then
    if [ -n "$ZSH_VERSION" ]; then
      VERSION_MAJOR="${match[1]}"
      VERSION_MINOR="${match[2]}"
      VERSION_PATCH="${match[3]}"
      VERSION_RC="${match[4]}"
    elif [ -n "$BASH_VERSION" ]; then
      VERSION_MAJOR="${BASH_REMATCH[1]}"
      VERSION_MINOR="${BASH_REMATCH[2]}"
      VERSION_PATCH="${BASH_REMATCH[3]}"
      VERSION_RC="${BASH_REMATCH[4]}"
    else
      echo "Unsupported shell type, only zsh and bash supported"
      exit 1
    fi

  else
    echo "unable to parse version string ${1}. Example of valid version string: 0.35.2rc1"
    exit 1
  fi
  export RABBITAI_VERSION="${VERSION_MAJOR}.${VERSION_MINOR}.${VERSION_PATCH}"
  export RABBITAI_RC="${VERSION_RC}"
  export RABBITAI_GITHUB_BRANCH="${VERSION_MAJOR}.${VERSION_MINOR}"
  export RABBITAI_PGP_FULLNAME="${2}"
  export RABBITAI_VERSION_RC="${RABBITAI_VERSION}rc${VERSION_RC}"
  export RABBITAI_RELEASE=apache-rabbitai-"${RABBITAI_VERSION}"
  export RABBITAI_RELEASE_RC=apache-rabbitai-"${RABBITAI_VERSION_RC}"
  export RABBITAI_RELEASE_TARBALL="${RABBITAI_RELEASE}"-source.tar.gz
  export RABBITAI_RELEASE_RC_TARBALL="${RABBITAI_RELEASE_RC}"-source.tar.gz
  export RABBITAI_TMP_ASF_SITE_PATH="/tmp/incubator-rabbitai-site-${RABBITAI_VERSION}"

  echo -------------------------------
  echo Set Release env variables
  env | grep ^RABBITAI_
  echo -------------------------------
fi
