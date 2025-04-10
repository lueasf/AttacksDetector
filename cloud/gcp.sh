#!/bin/bash

PROJECT_ID="attakx"
REGION="europe-west9"
REPO_NAME="attakx-repo"
IMAGE_NAME="attakx"
IMAGE_TAG="latest"
SERVICE_NAME="attakx-service"

# Build et push sur Artifact Registry
gcloud builds submit --tag ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG} .

# Deploy on Cloud Run
gcloud run deploy $SERVICE_NAME \
  --image ${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${IMAGE_NAME}:${IMAGE_TAG} \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --memory 2Gi \
  --cpu 1