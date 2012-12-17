cd client
hem build
echo 'window.isProduction=true; ' | cat - public/application.js > /tmp/out && mv /tmp/out public/application.js