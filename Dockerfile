FROM python:3.9-slim as builder

# install dependencies required to build python packages
RUN apt-get update

# setup venv
ENV VENV="/venv"
ENV PATH="${VENV}/bin:${PATH}"

# copy  build dependencies
COPY opnsense_cli/__init__.py /app/opnsense_cli/__init__.py
COPY MANIFEST.in /app/MANIFEST.in
COPY README.md /app/README.md
COPY setup.py /app/setup.py
COPY requirements.txt /app/requirements.txt
COPY test_requirements.txt /app/test_requirements.txt

WORKDIR /app

# install dependencies into builder venv
RUN python -m venv ${VENV} && ${VENV}/bin/pip3 install --upgrade pip setuptools wheel
RUN ${VENV}/bin/pip3 install --no-cache-dir -r requirements.txt
RUN ${VENV}/bin/pip3 install --no-cache-dir -r test_requirements.txt


FROM python:3.9-slim as app

RUN apt-get update \
    # some comfort...
    && apt-get install -y procps net-tools vim htop \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get autoremove -y \
    && apt-get clean -y

# copy dependencies from the builder stage
ENV VENV="/venv"
ENV PATH="${VENV}/bin:$PATH"
COPY --from=builder ${VENV} ${VENV}

# copy app files
COPY opnsense_cli /app/opnsense_cli
COPY ./acceptance_tests /app/acceptance_tests
COPY ./scripts /app/scripts
COPY MANIFEST.in /app/MANIFEST.in
COPY README.md /app/README.md
COPY .coveragerc /app/.coveragerc
COPY setup.py /app/setup.py


# Creates a non-root user and adds permission to access the /app folder
RUN addgroup --system appgroup && useradd appuser -g appgroup -m && chown -R appuser:appgroup /app

COPY docker/.opn-cli/conf.yaml /home/appuser/.opn-cli/conf.yaml
COPY docker/.opn-cli/ca.pem /home/appuser/.opn-cli/ca.pem

WORKDIR /app

# install app
RUN python -m venv ${VENV} && ${VENV}/bin/pip3 install --upgrade --no-cache-dir .

COPY requirements.txt /app/requirements.txt
COPY test_requirements.txt /app/test_requirements.txt

# run app
USER appuser
ENTRYPOINT ["opn-cli"]
