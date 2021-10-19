#!/usr/bin/env bash

set -eo pipefail

SHA=$(git rev-parse HEAD)
REPO_NAME="psbsgic/rabbitai"

if [[ "${GITHUB_EVENT_NAME}" == "pull_request" ]]; then
  REFSPEC=$(echo "${GITHUB_HEAD_REF}" | sed 's/[^a-zA-Z0-9]/-/g' | head -c 40)
  PR_NUM=$(echo "${GITHUB_REF}" | sed 's:refs/pull/::' | sed 's:/merge::')
  LATEST_TAG="pr-${PR_NUM}"
elif [[ "${GITHUB_EVENT_NAME}" == "release" ]]; then
  REFSPEC=$(echo "${GITHUB_REF}" | sed 's:refs/tags/::' | head -c 40)
  LATEST_TAG="${REFSPEC}"
else
  REFSPEC=$(echo "${GITHUB_REF}" | sed 's:refs/heads/::' | sed 's/[^a-zA-Z0-9]/-/g' | head -c 40)
  LATEST_TAG="${REFSPEC}"
fi

if [[ "${REFSPEC}" == "master" ]]; then
  LATEST_TAG="latest"
fi

cat<<EOF
  Rolling with tags:
  - ${REPO_NAME}:${SHA}
  - ${REPO_NAME}:${REFSPEC}
  - ${REPO_NAME}:${LATEST_TAG}
EOF

#
# Build the "lean" image
#
docker build --target lean \
  -t "${REPO_NAME}:${SHA}" \
  -t "${REPO_NAME}:${REFSPEC}" \
  -t "${REPO_NAME}:${LATEST_TAG}" \
  --label "sha=${SHA}" \
  --label "built_at=$(date)" \
  --label "target=lean" \
  --label "build_actor=${GITHUB_ACTOR}" \
  .

#
# Build the dev image
#
docker build --target dev \
  -t "${REPO_NAME}:${SHA}-dev" \
  -t "${REPO_NAME}:${REFSPEC}-dev" \
  -t "${REPO_NAME}:${LATEST_TAG}-dev" \
  --label "sha=${SHA}" \
  --label "built_at=$(date)" \
  --label "target=dev" \
  --label "build_actor=${GITHUB_ACTOR}" \
  .

if [ -z "${DOCKERHUB_TOKEN}" ]; then
  # Skip if secrets aren't populated -- they're only visible for actions running in the repo (not on forks)
  echo "Skipping Docker push"
else
  # Login and push
  docker logout
  docker login --username "${DOCKERHUB_USER}" --password "${DOCKERHUB_TOKEN}"
  docker push --all-tags "${REPO_NAME}"
fi
