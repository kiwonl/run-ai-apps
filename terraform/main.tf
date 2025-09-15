data "google_project" "project" {
}

# Enable necessary Google Cloud APIs for the project
resource "google_project_service" "default" {
  project = data.google_project.project.project_id
  
  for_each = toset([
    "dns.googleapis.com",               # Google Cloud DNS API
    "aiplatform.googleapis.com",        # Vertex AI API
    "servicedirectory.googleapis.com",  # Service Directory API
    "run.googleapis.com",               # Cloud Run API
    "cloudbuild.googleapis.com",        # Cloud Build API
    "artifactregistry.googleapis.com"   # Artifact Registry API
  ])

  service            = each.value
  disable_on_destroy = false
}