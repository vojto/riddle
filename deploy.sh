rsync -a . vojto@rinik.net:/var/www/apps/riddle
ssh vojto@rinik.net "cd /var/www/apps/riddle/server && forever stop -c python run.py && forever start -c python run.py"