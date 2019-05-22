#!/usr/bin/env bash
#!/bin/sh
repos=("/home/groupm/mediaops-project/mediaops/")

echo ""
echo "Getting latest for" ${#repos[@]} "repositories using pull --rebase"

for repo in "${repos[@]}"
do
  echo ""
  echo "****** Getting latest for" ${repo} "******"
  cd "${repo}"
  git pull --rebase
  echo "******************************************"
done
python /home/groupm/mediaops-project/mediaops/Classes/NdpTickets/MainNDP.py
