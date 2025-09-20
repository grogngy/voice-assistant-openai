# Deployment Workflow for Google Cloud Run

This document provides step-by-step instructions for deploying the Voice Assistant OpenAI application to Google Cloud Run.

## 🚀 Prerequisites

1. **Google Cloud Project Setup**
   ```bash
   # Create a new project (if needed)
   gcloud projects create your-project-id
   
   # Set the project
   gcloud config set project your-project-id
   
   # Enable billing for the project
   ```

2. **Enable Required APIs**
   ```bash
   gcloud services enable \
     speech.googleapis.com \
     texttospeech.googleapis.com \
     run.googleapis.com \
     cloudbuild.googleapis.com \
     containerregistry.googleapis.com
   ```

3. **Authentication Setup**
   ```bash
   # Login to Google Cloud
   gcloud auth login
   
   # Set up application default credentials
   gcloud auth application-default login
   ```

## 🔧 Environment Configuration

### 1. Local Environment Variables (.env)
```bash
# Copy template and configure
cp .env.example .env

# Required variables for production:
OPENAI_API_KEY=your_openai_api_key_here
GOOGLE_CLOUD_PROJECT=your-project-id
FLASK_ENV=production
SECRET_KEY=your-production-secret-key
```

### 2. Google Cloud Secret Manager (Recommended for Production)
```bash
# Store secrets in Secret Manager
echo -n "your_openai_api_key" | gcloud secrets create openai-api-key --data-file=-
echo -n "your-secret-key" | gcloud secrets create flask-secret-key --data-file=-

# Grant Cloud Run access to secrets
gcloud projects add-iam-policy-binding your-project-id \
    --member="serviceAccount:your-project-number-compute@developer.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

## 📦 Deployment Methods

### Method 1: Automated Deployment Script (Recommended)

```bash
# Make the script executable
chmod +x scripts/deploy.sh

# Deploy to Cloud Run
./scripts/deploy.sh
```

### Method 2: Manual Deployment

#### Step 1: Build and Push Container
```bash
# Set variables
PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="voice-assistant-openai"
REGION="us-central1"

# Build the container
gcloud builds submit --tag gcr.io/$PROJECT_ID/$SERVICE_NAME

# Or build locally and push
docker build -t gcr.io/$PROJECT_ID/$SERVICE_NAME .
docker push gcr.io/$PROJECT_ID/$SERVICE_NAME
```

#### Step 2: Deploy to Cloud Run
```bash
gcloud run deploy $SERVICE_NAME \
    --image gcr.io/$PROJECT_ID/$SERVICE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 2 \
    --max-instances 10 \
    --set-env-vars "FLASK_ENV=production,GOOGLE_CLOUD_PROJECT=$PROJECT_ID"
```

### Method 3: Continuous Deployment with GitHub Actions

1. **Set up GitHub Secrets**
   - `GCP_PROJECT_ID`: Your Google Cloud project ID
   - `GCP_SA_KEY`: Service account key JSON

2. **Create Service Account**
   ```bash
   gcloud iam service-accounts create github-actions \
       --description="GitHub Actions service account" \
       --display-name="GitHub Actions"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
       --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/run.admin"
   
   gcloud projects add-iam-policy-binding $PROJECT_ID \
       --member="serviceAccount:github-actions@$PROJECT_ID.iam.gserviceaccount.com" \
       --role="roles/storage.admin"
   
   gcloud iam service-accounts keys create key.json \
       --iam-account="github-actions@$PROJECT_ID.iam.gserviceaccount.com"
   ```

3. **Push to GitHub**
   ```bash
   git push origin main
   ```

## 🌐 Custom Domain Setup

### 1. Map Custom Domain
```bash
gcloud run domain-mappings create \
    --service voice-assistant-openai \
    --domain your-domain.com \
    --region us-central1
```

### 2. SSL Certificate
Google Cloud Run automatically provides SSL certificates for custom domains.

## 📊 Monitoring and Logging

### 1. View Logs
```bash
# Stream logs
gcloud logs tail projects/$PROJECT_ID/logs/run.googleapis.com

# View specific service logs
gcloud run services logs read voice-assistant-openai \
    --region=us-central1 \
    --limit=50
```

### 2. Monitoring Setup
```bash
# Enable monitoring
gcloud services enable monitoring.googleapis.com

# Create alerting policies (optional)
gcloud alpha monitoring policies create --policy-from-file=monitoring-policy.yaml
```

## 🔒 Security Best Practices

### 1. Environment Variables
- Never commit secrets to version control
- Use Google Secret Manager for production secrets
- Rotate secrets regularly

### 2. IAM and Authentication
```bash
# Create least-privilege service account
gcloud iam service-accounts create voice-assistant-sa \
    --description="Voice Assistant service account"

# Grant only necessary permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:voice-assistant-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/speech.editor"
```

### 3. Network Security
```bash
# Deploy with authentication required (if needed)
gcloud run deploy voice-assistant-openai \
    --image gcr.io/$PROJECT_ID/voice-assistant-openai \
    --no-allow-unauthenticated
```

## 🚨 Troubleshooting

### Common Issues and Solutions

#### 1. Build Failures
```bash
# Check build logs
gcloud builds list --limit=5

# View specific build
gcloud builds log [BUILD_ID]
```

#### 2. Memory Issues
```bash
# Increase memory allocation
gcloud run services update voice-assistant-openai \
    --memory 4Gi \
    --region us-central1
```

#### 3. Cold Start Issues
```bash
# Set minimum instances
gcloud run services update voice-assistant-openai \
    --min-instances 1 \
    --region us-central1
```

#### 4. Permission Errors
```bash
# Check service account permissions
gcloud projects get-iam-policy $PROJECT_ID

# Add missing permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:SERVICE_ACCOUNT_EMAIL" \
    --role="REQUIRED_ROLE"
```

## 📈 Scaling and Performance

### 1. Auto-scaling Configuration
```bash
gcloud run services update voice-assistant-openai \
    --min-instances 0 \
    --max-instances 100 \
    --concurrency 80 \
    --cpu-throttling \
    --region us-central1
```

### 2. Performance Monitoring
- Use Google Cloud Monitoring
- Set up custom metrics for response time
- Monitor error rates and success rates

## 🔄 Update Workflow

### 1. Rolling Updates
```bash
# Deploy new version
gcloud run deploy voice-assistant-openai \
    --image gcr.io/$PROJECT_ID/voice-assistant-openai:new-version \
    --region us-central1

# Traffic splitting (for gradual rollout)
gcloud run services update-traffic voice-assistant-openai \
    --to-revisions=new-revision=50,old-revision=50 \
    --region us-central1
```

### 2. Rollback
```bash
# List revisions
gcloud run revisions list --service=voice-assistant-openai --region=us-central1

# Rollback to previous revision
gcloud run services update-traffic voice-assistant-openai \
    --to-latest \
    --region us-central1
```

## 📋 Deployment Checklist

- [ ] Google Cloud project created and configured
- [ ] Required APIs enabled
- [ ] Service account created with proper permissions
- [ ] Secrets stored in Secret Manager
- [ ] Environment variables configured
- [ ] Application tested locally
- [ ] Docker image builds successfully
- [ ] Cloud Run service deployed
- [ ] Custom domain configured (if applicable)
- [ ] Monitoring and logging set up
- [ ] Security policies reviewed
- [ ] Load testing completed
- [ ] Backup and disaster recovery plan in place

## 🔗 Useful Commands

```bash
# Quick deployment
./scripts/deploy.sh

# Check service status
gcloud run services describe voice-assistant-openai --region=us-central1

# View service URL
gcloud run services list --filter="metadata.name:voice-assistant-openai"

# Delete service (if needed)
gcloud run services delete voice-assistant-openai --region=us-central1
```