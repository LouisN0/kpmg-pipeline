#!/bin/bash

# Build docker images
docker build --no-cache -f dags/kpmg-pipeline/scraper/Dockerfile -t scraper:latest ./dags/kpmg-pipeline;
docker build --no-cache -f dags/kpmg-pipeline/text_extractor/Dockerfile -t text_extractor:latest ./dags/kpmg-pipeline;
docker build --no-cache -f dags/kpmg-pipeline/classification/Dockerfile -t classification:latest ./dags/kpmg-pipeline;
docker build --no-cache -f dags/kpmg-pipeline/summary/Dockerfile -t summary:latest ./dags/kpmg-pipeline;

# Init Airflow
docker compose up airflow-init;
# Run Airflow
docker compose --env-file .env up;