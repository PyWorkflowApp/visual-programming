FROM python:3.8.2

WORKDIR /visual-programming/back-end

COPY Pipfile Pipfile.lock ./
COPY CLI/ ./CLI/
COPY pyworkflow/ ./pyworkflow/

RUN pip install pipenv
RUN pipenv install --dev --ignore-pipfile

COPY . ./vp/

EXPOSE 8000

WORKDIR /visual-programming/back-end/vp

CMD pipenv run manage.py runserver 0.0.0.0:8000
