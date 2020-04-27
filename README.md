# visual-programming

So far the app comprises a Django app and a SPA React app (bootstrapped with
create-react-app). For React to request data from Django, the `proxy` field is
set in `front-end/package.json`, telling the dev server to fetch non-static
data from `localhost:8000` **where the Django app must be running**.

## Django

### Install Dependencies
1. Install `pipenv` from home directory

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

4. Activate and exit the shell

    - `pipenv shell`
    - `exit`

5. Or, run single commands

    - `pipenv run python [COMMAND]`

### Installing new packages
- Simply install via: `pipenv install [package-name]`

### Create dotenv file with app secret and dev environment
- `echo "SECRET_KEY='TEMPORARY SECRET KEY'" > vp/.env`
- `echo "DJANGO_ENV='development'" > vp/.env`

### Build and collect static files from front-end
- `cd front-end`
- `npm run build`
- `cd ../vp`
- `python manage.py collectstatic --noinput`

### Start dev server from back-end root (./vp)
- `waitress-serve vp.wsgi:application`
<!-- - `pipenv run DJANGO_ENV=development python manage.py runserver`
  - only `DJANGO_ENV=development python manage.py runserver` may be required if pipenv has created the virtualenv in your terminal -->

---
## React

### Install Prerequisites
- `cd front-end`
- `npm install`

### Start dev server
- `npm start`

---
## CLI
1. Run pipenv shell.
2. Create a workflow using UI and save it. 
3. Run it as: pyworkflow --file-directory (path-to-json-workflow-file) execute

---
## Tests
PyWorkflow currently has two sets of tests: API endpoints and unit tests.
The API tests are written in Postman and can be run individually, by importing
the collection and environment into your Postman application, or via the command
line by [installing Newman](https://www.npmjs.com/package/newman) and running:

- `cd Postman`
- `newman run PyWorkflow-runner.postman_collection.json --environment Local-env.postman_environment.json`

Unit tests for the PyWorkflow package are run using Python's built-in `unittest`
package.

- `cd pyworkflow/pyworkflow`
- `pipenv run python3 -m unittest tests/*.py`

