# Python-Web-Scraping-Data-Automation-Tool

A Python-based web scraping and data automation tool that collects data from websites, cleans/processes it, and exports it into CSV/Excel/Google Sheets automatically on a schedule. The tool supports error handling, logging, scheduling, and modular scrapers for multiple websites.

## AIRFLOW

This project can be run hourly using apache airflow docker container. To do that run the following:

### How to Run

1- Navigate to airflow/ folder:

```cd airflow```

2- Build Docker images:

```docker-compose build```

3- Start services:

```docker-compose up -d```

4- Access Airflow UI: <http://localhost:8080>

5- Enable your DAG crypto_stock_pipeline and trigger manually or let it run on schedule.
