cp client/public/index.html server/riddle/templates/index.html
cd client
hem build
echo 'window.isProduction=true; ' | cat - public/application.js > /tmp/out && mv /tmp/out public/application.js