ARG PYTHON_VERSION
FROM ${PYTHON_VERSION:?err}

WORKDIR /library

COPY . .

RUN sh scripts/install

EXPOSE 8000
