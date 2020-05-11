FROM python:3.8

WORKDIR /visual-programming/back-end

COPY Pipfile Pipfile.lock ./
COPY CLI/ ./CLI/
COPY pyworkflow/ ./pyworkflow/

RUN pip install pipenv
RUN pipenv install --ignore-pipfile

COPY vp/ ./vp

EXPOSE 8000

WORKDIR /visual-programming/back-end/vp
