# Tests

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

To see coverage, you can use the `coverage` package. This is included in the Pipfile
but must be installed with `pipenv install -dev`. Then, while still in the pyworkflow
directory, you can run

- `coverage run -m unittest tests/*.py`
- `coverage report` (to see a report via the CLI)
- `coverage html && open /htmlcov/index.html` (to view interactive coverage)
