from python:3.12

workdir /var/www/

copy ./src ./src
copy ./pyproject.toml .
run pip install poetry
run poetry install --no-dev
