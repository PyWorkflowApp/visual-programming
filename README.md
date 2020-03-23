# visual-programming

So far the app comprises a Django app and a SPA React app (bootstrapped with
create-react-app). For React to request data from Django, the `proxy` field is
set in `front-end/package.json`, telling the dev server to fetch non-static
data from `localhost:8000` **where the Django app must be running**.

## Django

### Install Dependencies
1. Install `pipenv`

    - **Homebrew**:

        - `brew install pipenv`

    - **pip**:

        - `pip install pipenv`
        - or depending on your versioning setup:
        - `pip3 install pipenv`

        - You can install at the User level using **pip** via: `pip install --user pipenv`

2. `cd` to top level of project (contains `Pipfile` and `Pipefile.lock`)

3. Install dependencies

    - `pipenv install`

### Installing new packages
- Simply install via: `pipenv install [package-name]`

### Create dotenv file with app secret
- `echo "SECRET_KEY='TEMPORARY SECRET KEY'" > vp/.environment`

### Start dev server from app root
- `cd vp`
- `python manage.py runserver`

---
## React

### Install Prerequisites
- `cd front-end`
- `npm install`

### Start dev server
- `npm start`
