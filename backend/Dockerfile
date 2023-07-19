FROM python:3.11-slim-buster

RUN pip install poetry
COPY app /application
WORKDIR /application

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

ADD entrypoint.sh /
ENV TEST_FIELD="$TEST"
RUN ["chmod", "+x", "/entrypoint.sh"]
ENTRYPOINT /entrypoint.sh $TEST_FIELD
