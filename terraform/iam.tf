# Cloud Run 을 위한 Service Account
resource "google_service_account" "sa" {
  project      = var.project_id
  account_id   = var.run_service_account
  display_name = "google_service_account"
}

# Cloud Run SA에 권한 추가 - AIplatform AI
resource "google_project_iam_member" "ai_platform_user" {
  project = var.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

# Cloud Run SA에 권한 추가 - Run Invoker
resource "google_project_iam_member" "run_invoker" {
  project = var.project_id
  role    = "roles/run.invoker"
  member  = "serviceAccount:${google_service_account.sa.email}"
}

# Cloud Build 를 위한 Service Account
data "google_project_service_identity" "cloudbuild_sa" {
  provider = google
  project  = var.project_id
  service  = "cloudbuild.googleapis.com"
}

# Cloud Build SA 에 권한 추가 - Cloud Run Administrator
resource "google_project_iam_member" "cloud_build_run_admin" {
  project = var.project_id
  role    = "roles/run.admin"
  member  = "serviceAccount:${data.google_project_service_identity.cloudbuild_sa.email}"
}

# Cloud Build SA 에 권한 추가 - ServiceAccountUser
resource "google_project_iam_member" "cloud_build_service_account_user" {
  project = var.project_id
  role    = "roles/iam.serviceAccountUser"
  member  = "serviceAccount:${data.google_project_service_identity.cloudbuild_sa.email}"
}

# Cloud Build SA 에 권
# Cloud Build SA 에 권한 추가 - Cloud Build Builder
resource "google_project_iam_member" "cloud_build_builds_builder" {
  project = var.project_id
  role    = "roles/cloudbuild.builds.builder"
  member  = "serviceAccount:${data.google_project_service_identity.cloudbuild_sa.email}"
}