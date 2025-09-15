# Movie Recommendation AI Agent

This project is a movie recommendation AI agent that uses Google's Gemini model to provide movie recommendations based on user input. The application can be deployed to either Google Kubernetes Engine (GKE) or Cloud Run.

## Key Components

*   **AI Agent:** A Python application using the Gemini Large Language Model to generate movie recommendations.
*   **Deployment:** Options for deploying the application on both GKE and Cloud Run.
*   **Infrastructure as Code:** Terraform scripts to provision the necessary Google Cloud resources.

## Getting Started

### Prerequisites

*   A Google Cloud project.
*   `gcloud` CLI installed and configured.
*   `kubectl` installed.
*   `git` installed.

### 1. Environment Setup

#### Activate Services
```
gcloud services enable \
 cloudbuild.googleapis.com \
 aiplatform.googleapis.com \
 run.googleapis.com \
 container.googleapis.com \
 artifactregistry.googleapis.com \
 --project $PROJECT_ID
```

#### Set Environment Variables
```
export PROJECT_ID=$GOOGLE_CLOUD_PROJECT
export REGION=us-central1

export CLUSTER=mr-gke

export K8S_SERVICE_ACCOUNT=mr-ksa
export GCP_SERVICE_ACCOUNT=mr-gsa

export GEMINI_MODEL=gemini-1.5-flash-002
```

### 2. Build and Deploy

#### Clone the repository
```
git clone https://github.com/kiwonl/movie-recommendation
cd ~\/movie-recommendation
```

#### Build the container image
```
gcloud artifacts repositories create docker-repo \
  --repository-format=docker \
  --location=$REGION \
  --description="Docker repository" \
  --project=$PROJECT_ID

gcloud builds submit --tag=${REGION}-docker.pkg.dev/${PROJECT_ID}/docker-repo/movie-recommendation
```

### 3. Deployment Options

You can deploy the application to either GKE or Cloud Run.

#### Option A: Deploy to Google Kubernetes Engine (GKE)

##### Create GKE Cluster
```
gcloud container clusters create-auto $CLUSTER \
    --location=$REGION --async
```

##### Authenticate to GKE Cluster
```
gcloud container clusters get-credentials $CLUSTER --region $REGION
```

##### Configure and Deploy to GKE
```
sed -i 's/${K8S_SERVICE_ACCOUNT}/'${K8S_SERVICE_ACCOUNT}'/g' k8s.yaml
sed -i 's/${REGION}/'${REGION}'/g' k8s.yaml
sed -i 's/${PROJECT_ID}/'${PROJECT_ID}'/g' k8s.yaml
sed -i 's/${GEMINI_MODEL}/'${GEMINI_MODEL}'/g' k8s.yaml

# Workload Identity Federation for GKE
gcloud iam service-accounts create ${GCP_SERVICE_ACCOUNT} \
 --project ${PROJECT_ID}

gcloud projects add-iam-policy-binding ${PROJECT_ID}  \
 --member "serviceAccount:${GCP_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com"  \
 --role "roles/aiplatform.user"

gcloud iam service-accounts add-iam-policy-binding ${GCP_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com \
 --role roles/iam.workloadIdentityUser \
 --member "serviceAccount:${PROJECT_ID}.svc.id.goog[default/${K8S_SERVICE_ACCOUNT}]"

kubectl annotate serviceaccount ${K8S_SERVICE_ACCOUNT} \
iam.gke.io/gcp-service-account=${GCP_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com

# Deploy
kubectl apply -f k8s.yaml
```

##### Test the GKE deployment
```
export ENDPOINT=[External-ip of Service]

curl -X POST -H "Content-Type: application/json" -d '{
  "movies": ["Despicable Me 4", "Inside Out 2"],
  "scenario": "가족들과 함께 보기 좋은"
}' "$ENDPOINT/recommendations"
```

#### Option B: Deploy to Cloud Run

##### Deploy the service
```
gcloud run deploy mr-run \
--image ${REGION}-docker.pkg.dev/${PROJECT_ID}/docker-repo/movie-recommendation  \
--region ${REGION}  \
--set-env-vars PROJECT_ID=${PROJECT_ID},REGION=${REGION},GEMINI_MODEL=${GEMINI_MODEL} \
--service-account ${GCP_SERVICE_ACCOUNT}@${PROJECT_ID}.iam.gserviceaccount.com  \
--allow-unauthenticated
```

##### Test the Cloud Run deployment
```
export ENDPOINT=[Endpoint of Cloud Run Service]

curl -X POST -H "Content-Type: application/json" -d '{
  "movies": ["Despicable Me 4", "Inside Out 2"],
  "scenario": "가족들과 함께 보기 좋은"
}' "$ENDPOINT/recommendations"
```