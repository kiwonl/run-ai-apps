# Gemini Movie Recommendation App

## Overview

This project is a movie recommendation web application that uses Google's Gemini model. Users can input a list of movies and a scenario, and the AI will recommend the most suitable movie.

The application is designed to be deployed on **Google Cloud Run**.

## Getting Started

### Prerequisites

- You must complete the infrastructure setup with Terraform before proceeding with the deployment steps below.

### Application Deployment to Cloud Run

1.  **Set deployment environment variables:**

    ```bash
    cd ../gemini-app

    export PROJECT_ID=<your-gcp-project-id>
    export PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")
    export REGION=us-central1

    export NETWORK_NAME=run-ai-apps-network
    export SUBNET_NAME=run-ai-apps-subnet
    export SERVICE_ACCOUNT=run-ai-apps-sa

    # You can choose other Gemini models if you prefer
    export GEMINI_MODEL=gemini-1.5-flash
    ```

2.  **Deploy the application:**

    This command builds the container image from the source code and deploys it to Cloud Run.

    ```bash
    gcloud run deploy gemini-movie-app \
        --source . \
        --region ${REGION} \
        --service-account ${SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
        --allow-unauthenticated \
        --set-env-vars PROJECT_ID=${PROJECT_ID},REGION=${REGION},GEMINI_MODEL=${GEMINI_MODEL} \
        --network=${NETWORK_NAME} \
        --subnet=${SUBNET_NAME} \
        --vpc-egress=all-traffic
    ```

3.  **Test the Deployment:**
Once deployed, `gcloud` will provide a service URL. Use this URL to test the API endpoint.

1.  **Set the endpoint URL:**

    Replace `<service-url-from-gcloud-output>` with the actual URL of your Cloud Run service.

    ```bash
    export ENDPOINT=<service-url-from-gcloud-output>
    ```

2.  **Send a test request using `curl`:**

    ```bash
    curl -X POST -H "Content-Type: application/json" -d 
    {
      "movies": ["Demon Slayer: Kimetsu no Yaiba The Movie: Infinity Castle", "KPop Demon Hunters"],
      "scenario": "가족들과 함께 보기 좋은"
    }
    " $ENDPOINT/recommendations"
    ```

    You should receive a JSON response with a movie recommendation.
