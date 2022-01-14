# This Dockerfile should be centralised within your organisation, such that is can be used
# for all model CI/CD pipelines.

# Create three layers: base, testing, and final.
# With this setup, the resulting container will not contain tests and checks
# that are required for CI, such as pytest/pylint.

#
# Base layer
#
FROM python:3.9-slim-buster AS base

WORKDIR /code

# Add project files.
ADD setup.py .
ADD src/ src/
ADD .pylintrc .

# Create venv in /opt/venv
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install .

#
# Testing layer
#
FROM python:3.9-slim-buster AS ci

WORKDIR /code

ADD tests/ tests/

COPY --from=base /code .
COPY --from=base /opt/venv /opt/venv
COPY --from=base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

ADD requirements-dev.txt .

RUN /opt/venv/bin/pip install -r requirements-dev.txt \
    && /opt/venv/bin/pip install pytest pylint

RUN /opt/venv/bin/pytest tests/
RUN /opt/venv/bin/pylint --fail-under 9.0 src/


#
# Final layer
#
FROM python:3.9-slim-buster

WORKDIR /code

COPY --from=base /code .
COPY --from=base /opt/venv /opt/venv
COPY --from=base /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

ENTRYPOINT ["/opt/venv/bin/vaidemo"]
