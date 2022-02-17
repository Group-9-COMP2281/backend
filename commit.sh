#!/bin/bash

(pip freeze > requirements.txt) > /dev/null 2>&1
if [ $? -ne 0 ]; then
  echo "pip freeze failed."
  exit 1
fi

git add -A
git commit -a

printf "\n\nCommit finished."
