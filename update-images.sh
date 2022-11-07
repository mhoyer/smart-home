#!/bin/bash

# getting docker tags, see: https://stackoverflow.com/a/39454426
# semver sorting, see: https://stackoverflow.com/a/63027058

function fetch_tags() {
  image="$1"
  default_pattern='^[0-9]+\.[0-9]+$'
  pattern="${2:-$default_pattern}"
  docker_response=$(wget -q https://registry.hub.docker.com/v2/repositories/${image}/tags?page_size=30 -O -)
  all_tags=$(
    echo "${docker_response}" \
    | jq -r '.results[].name'
  )
  if [ -z "${all_tags}"]; then
    echo "${docker_response}"
    echo
    echo "Unable to parse JSON response above from https://registry.hub.docker.com/v1/repositories/${image}/tags."
    exit 1
  fi

  matching_tags=$(
    echo "${all_tags}" \
    | grep -E "$pattern" \
    | sort -t "." -k1,1n -k2,2n -k3,3n
  )
  latest_tag=$(echo "$matching_tags" | tail -n1)

  if [ -z "$latest_tag" ]; then
    echo "${all_tags}"
    echo
    echo "Unable to find a matching tag from all tags found  above from https://registry.hub.docker.com/v1/repositories/${image}/tags."
    exit 1
  fi

  echo "found $1:$latest_tag (matching the pattern of '$pattern')"
  sed -i "s|image: ${1}:.*|image: ${1}:${latest_tag}|g" docker-compose.yml
}

fetch_tags koenkk/zigbee2mqtt '^[0-9]+\.[0-9]+\.[0-9]+$'
fetch_tags homeassistant/raspberrypi4-homeassistant '^[0-9]+\.[0-9]+\.[0-9]+$'

git diff docker-compose.yml

