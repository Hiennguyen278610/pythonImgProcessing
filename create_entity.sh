#!/bin/bash
# filepath: create_entity.sh

if [ "$1" != "py" ] || [ -z "$2" ]; then
  echo "Usage: $0 py <EntityName>"
  exit 1
fi

ENTITY="$2"
CAP_ENTITY="$(tr '[:lower:]' '[:upper:]' <<< ${ENTITY:0:1})${ENTITY:1}"
LOW_ENTITY="$(tr '[:upper:]' '[:lower:]' <<< ${ENTITY:0:1})${ENTITY:1}"

BASE_DIR="src"

declare -A PATHS=(
  ["model"]="$BASE_DIR/model/${CAP_ENTITY}.py"
  ["service"]="$BASE_DIR/service/${CAP_ENTITY}Service.py"
  ["repository"]="$BASE_DIR/repository/${CAP_ENTITY}Repository.py"
  ["controller"]="$BASE_DIR/controller/${CAP_ENTITY}Controller.py"
  ["view"]="$BASE_DIR/view/${CAP_ENTITY}Panel.py"
)

declare -A CONTENTS=(
  ["model"]="class ${CAP_ENTITY}:\n    def __init__(self):\n        pass\n"
  ["service"]="class ${CAP_ENTITY}Service:\n    def __init__(self):\n        pass\n"
  ["repository"]="class ${CAP_ENTITY}Repository:\n    def __init__(self):\n        pass\n"
  ["controller"]="class ${CAP_ENTITY}Controller:\n    def __init__(self):\n        pass\n"
  ["view"]="class ${CAP_ENTITY}Panel:\n    def __init__(self, master, **kwargs):\n        pass\n"
)

for key in "${!PATHS[@]}"; do
  FILE="${PATHS[$key]}"
  DIR=$(dirname "$FILE")
  if [ ! -d "$DIR" ]; then
    mkdir -p "$DIR"
  fi
  if [ ! -f "$FILE" ]; then
    echo -e "${CONTENTS[$key]}" > "$FILE"
    echo "Created $FILE"
  else
    echo "$FILE already exists, skipped."
  fi
done