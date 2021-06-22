#!/bin/bash
user=${1-andeman}
project=${2- opn-cli}

docker run -it --rm  -v "$(pwd)":/usr/local/src/your-app \
githubchangeloggenerator/github-changelog-generator \
-t ${CHANGELOG_GITHUB_TOKEN} \
--user ${user} \
--project ${project}
