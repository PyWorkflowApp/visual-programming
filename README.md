# visual-programming

So far the app comprises a Django app and a SPA React app (bootstrapped with
create-react-app). For React to request data from Django, the `proxy` field is
set in `front-end/package.json`, telling the dev server to fetch non-static
data from `localhost:8000` **where the Django app must be running**.

## Django

**Install Prerequisites**
- `pip install -r requirements.txt`

**Create dotenv file with app secret**
- `echo "SECRET_KEY='TEMPORARY SECRET KEY'" > .environment`

**Start dev server from app root**
- `cd vp`
- `python manage.py runserver`


## React
**Install Prerequisites**
- `cd front-end`
- `npm install`

**Start dev server**
- `npm start`
