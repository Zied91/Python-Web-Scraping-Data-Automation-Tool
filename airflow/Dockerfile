FROM apache/airflow:slim-latest

# Set environment
ENV AIRFLOW_HOME=/opt/airflow

# Copy your project code (scrapers, utils, data, config)
COPY ../ /opt/airflow/stock_crypto_tracker/

# Install Python dependencies for your project
COPY ../requirements.txt .
RUN pip install -r requirements.txt

# Set Airflow entrypoint
USER airflow
