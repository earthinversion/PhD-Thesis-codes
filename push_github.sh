#!/bin/bash
# git pull
git status
echo "Do you want to CONTINUE?"
read response
if [ "$response" = "yes" ]; then
git add .
git commit -m "version Sunday, June 7, 2020 at 11:02:54 AM"
git push origin master
fi