# Gemini Movie Recommendation App

## Overview

This project is a movie recommendation web application that uses Google's Gemini model. Users can input a list of movies and a scenario, and the AI will recommend the most suitable movie.

The application is designed to be deployed on **Google Cloud Run**.

## Key Components

*   **Web Application:** A Python Flask application that serves a web interface and a REST API for recommendations.
*   **AI Model:** Utilizes Google's Gemini model via Vertex AI to generate movie recommendations.
*   **Infrastructure as Code:** Terraform scripts to provision the necessary Google Cloud resources (VPC Network, Service Account, etc.).

## Getting Started

Follow these steps to set up, provision, and deploy the application. All commands should be run from the `gemini-app` directory.

### 1. Prerequisites

*   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and authenticated.
*   [Terraform](https://learn.hashicorp.com/tutorials/terraform/install-cli) installed.

### 2. Infrastructure Setup (Terraform)

First, set up the necessary infrastructure using Terraform.

1.  **Set environment variables:**

    Replace `<your-gcp-project-id>` with your actual Google Cloud Project ID.

    ```bash
    export PROJECT_ID=<your-gcp-project-id>
    export REGION=us-central1
    ```

2.  **Update `terraform.tfvars`:**

    This command updates the Terraform variables file with your project ID and region.

    ```bash
    cd terraform && \
    sed -i \
    -e "s/your-gcp-project-id/$PROJECT_ID/" \
    -e "s/your-region/$REGION/" \
    terraform.tfvars
    ```

3.  **Initialize and apply Terraform:**

    This will provision the resources defined in the `.tf` files.

    ```bash
    terraform init
    terraform plan
    terraform apply --auto-approve
    ```

    After applying, Terraform will output the names of the created resources. Take note of these for the next step.

    ```
    Outputs:

    network_name = "gemini-app-vpc"
    service_account_account_id = "gemini-app-sa"
    subnetwork_name = "gemini-app-subnet"
    ```

### 3. Application Deployment (Cloud Run)

Now, deploy the application to Cloud Run.

1.  **Set deployment environment variables:**

    Use the outputs from the `terraform apply` command in the previous step.

    ```bash
    cd ..

    export NETWORK_NAME=<network_name_from_terraform_output>
    export SUBNET_NAME=<subnetwork_name_from_terraform_output>
    export SERVICE_ACCOUNT=<service_account_account_id_from_terraform_output>

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

### 4. Test the Deployment

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
      "movies": ["Despicable Me 4", "Inside Out 2", "The Godfather"],
      "scenario": "가족들과 함께 보기 좋은"
    }
    " $ENDPOINT/recommendations"
    ```

    You should receive a JSON response with a movie recommendation.
