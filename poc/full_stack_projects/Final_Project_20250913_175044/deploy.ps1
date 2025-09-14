# AI-generated deployment script (PowerShell version) - v3 (ASCII-only)

# Stop script on error
$ErrorActionPreference = "Stop"

Write-Host "🚀 Starting deployment for Final_Project_20250913_175044..."
Write-Host "--------------------------------------------------"

# --- Variables ---
$GCP_PROJECT_ID="denkojobcenter"
$GCP_REGION="asia-northeast1"
$FRONTEND_SERVICE_NAME="final-project-20250913-175044-frontend"
$BACKEND_SERVICE_NAME="final-project-20250913-175044-backend"

# --- Set GCP Project ---
Write-Host "1. Setting GCP project: $GCP_PROJECT_ID"
gcloud config set project $GCP_PROJECT_ID

# --- Deploy Frontend ---
Write-Host "`n2. Building and deploying frontend..."
Set-Location frontend

# Build Docker image
Write-Host "   - Building Docker image: $FRONTEND_SERVICE_NAME"
gcloud builds submit --tag "gcr.io/$GCP_PROJECT_ID/$FRONTEND_SERVICE_NAME"

# Deploy to Cloud Run
Write-Host "   - Deploying to Cloud Run: $FRONTEND_SERVICE_NAME"
gcloud run deploy $FRONTEND_SERVICE_NAME `
  --image "gcr.io/$GCP_PROJECT_ID/$FRONTEND_SERVICE_NAME" `
  --platform managed `
  --region $GCP_REGION `
  --port 80 `
  --allow-unauthenticated

Set-Location ..

# --- Deploy Backend ---
Write-Host "`n3. Building and deploying backend..."
Set-Location backend

# Build Docker image
Write-Host "   - Building Docker image: $BACKEND_SERVICE_NAME"
gcloud builds submit --tag "gcr.io/$GCP_PROJECT_ID/$BACKEND_SERVICE_NAME"

# Deploy to Cloud Run
Write-Host "   - Deploying to Cloud Run: $BACKEND_SERVICE_NAME"
gcloud run deploy $BACKEND_SERVICE_NAME `
  --image "gcr.io/$GCP_PROJECT_ID/$BACKEND_SERVICE_NAME" `
  --platform managed `
  --region $GCP_REGION `
  --allow-unauthenticated

Set-Location ..

Write-Host "--------------------------------------------------"
Write-Host "🎉 All deployments completed successfully!"

# Display Cloud Run URLs
$FRONTEND_URL = gcloud run services describe $FRONTEND_SERVICE_NAME --platform managed --region $GCP_REGION --format 'value(status.url)'
$BACKEND_URL = gcloud run services describe $BACKEND_SERVICE_NAME --platform managed --region $GCP_REGION --format 'value(status.url)'

Write-Host "   - Frontend URL: $FRONTEND_URL"
Write-Host "   - Backend URL: $BACKEND_URL"
