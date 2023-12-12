#!/bin/bash
#this is a shortcut for pushing alx project to github
loober=$(cat ~/counter.txt)
commit_message="Commit : $loober"
git add .
git commit -m "$commit_message"
git push
((loober++))
echo "$loober" > ../../counter.txt
