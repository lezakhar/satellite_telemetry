ARG AIRFLOW_VERSION="2.9.3"
ARG AIRFLOW_PYTHON_VERSION="python3.11"

FROM apache/airflow:${AIRFLOW_VERSION}-${AIRFLOW_PYTHON_VERSION}

USER root

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev && \
    apt-get install -y openjdk-17-jdk && \
    apt-get autoremove -yqq --purge && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64

COPY ./airflow_requirements.txt .
RUN pip install -r airflow_requirements.txt

USER root
