# test-file
just for test how to uploading a file on ubuntu

and the process as follows:

git init

git add *

git commit -m "version1.0"

git remote add origin https://github.com/Wisteriak/test-file.git

git push -u origin master


#
may be will use the next code when the README.md not exist at myGithub directory

git pull --rebase origin master

git push -u origin master


# the next code will be delete some file

git rm -r --cached test.py

git status

git commit -m"deleted"

git status

git push origin master
