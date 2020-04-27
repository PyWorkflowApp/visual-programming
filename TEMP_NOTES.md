# DevOps Libraries
`npm run build` > REPLACE WITH > webpack
Webpack: Bundles front-end assets into static bundle
  - `./node_modules/.bin/webpack --config webpack.config.js --watch`
    - watches for front-end changes during development; bundle && hot reload
Collectstatic: Copies bundle of statics to Django location to be served
  - `python manage.py collectstatic --noinput`
WhiteNoise: Allows app to serve its own static files w/o nginx or S3

# serve the back-end from `vp`
`waitress-serve vp.wsgi:application`
# start the front-end from `front-end`
`npm start`
# should show up on:
localhost:8080
# issue with websocket may be related to wsgi usage instead of asgi (Django Channels?)
** issue with websocket **
** also, not using webpack_loader via template **
