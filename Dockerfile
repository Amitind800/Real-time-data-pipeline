FROM apache/airflow:2.7.3

# Ensure pip is up-to-date
RUN pip install --no-cache-dir --upgrade pip

# Install correct version of openlineage provider
RUN pip install --no-cache-dir "apache-airflow-providers-openlineage>=1.8.0"

# (Optional) Install Spark provider if not already present
RUN pip install --no-cache-dir apache-airflow-providers-apache-spark
