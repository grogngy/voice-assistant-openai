# Google Cloud Live URL Guide

This document provides step-by-step instructions for deploying your Voice Assistant OpenAI to Google Cloud and getting the live URL.

## 🚀 Quick Deployment to Get Live URL

### 1. One-Command Deployment
```bash
# Deploy and get live URL in one step
./scripts/deploy.sh
```

After deployment completes, you'll see output like:
```
🎉 Deployment Complete!
=================================
🌐 Your Voice Assistant is now LIVE!
🔗 Live URL: https://voice-assistant-openai-xxxxx-uc.a.run.app
=================================
```

### 2. Get URL of Existing Deployment
```bash
# If already deployed, just get the URL
./scripts/get-url.sh
```

### 3. Manual URL Retrieval
```bash
# Get the URL manually
gcloud run services describe voice-assistant-openai \
    --region=us-central1 \
    --format="value(status.url)"
```

## 📋 Prerequisites for Going Live

### 1. Google Cloud Setup
```bash
# Install Google Cloud SDK if not already installed
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Login and set project
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Enable required APIs
gcloud services enable run.googleapis.com cloudbuild.googleapis.com
```

### 2. Environment Configuration
```bash
# Copy and configure environment variables
cp .env.example .env

# Required variables for production:
# OPENAI_API_KEY=your_api_key
# GOOGLE_CLOUD_PROJECT=your_project_id
# FLASK_ENV=production
# SECRET_KEY=your_secret_key
```

## 🌐 Deployment Options

### Option 1: Default Cloud Run (Recommended)
```bash
# Deploy with default settings
./scripts/deploy.sh
```
- ✅ Automatic HTTPS
- ✅ Serverless scaling
- ✅ Global CDN
- ✅ Free tier available

### Option 2: Custom Domain
```bash
# Deploy with custom domain
./scripts/deploy.sh

# Then map custom domain
gcloud run domain-mappings create \
    --service voice-assistant-openai \
    --domain yourdomain.com \
    --region us-central1
```

### Option 3: Enhanced Configuration
```bash
# Deploy with custom settings
gcloud run deploy voice-assistant-openai \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated \
    --memory 2Gi \
    --cpu 2 \
    --min-instances 1 \
    --max-instances 100
```

## 🔗 URL Management

### Access Your Live URLs
After deployment, your service will have these endpoints:

1. **Main Application**: `https://voice-assistant-openai-xxxxx-uc.a.run.app`
2. **Health Check**: `https://voice-assistant-openai-xxxxx-uc.a.run.app/health`
3. **Configuration**: `https://voice-assistant-openai-xxxxx-uc.a.run.app/config`

### URL Storage
The deployment scripts automatically save your URL to `.deployment-url` for easy access:
```bash
# Get saved URL
cat .deployment-url

# Open in browser (macOS)
open $(cat .deployment-url)

# Copy to clipboard (macOS)
cat .deployment-url | pbcopy
```

## 🔧 Managing Your Live Service

### Check Service Status
```bash
# View service details
gcloud run services describe voice-assistant-openai --region=us-central1

# Check health
curl https://your-service-url.run.app/health
```

### View Logs
```bash
# Stream live logs
gcloud logs tail projects/YOUR_PROJECT_ID/logs/run.googleapis.com

# View recent logs
gcloud run services logs read voice-assistant-openai --region=us-central1
```

### Update Deployment
```bash
# Deploy updates
./scripts/deploy.sh

# Update environment variables
gcloud run services update voice-assistant-openai \
    --set-env-vars "OPENAI_API_KEY=new_key" \
    --region=us-central1
```

### Scale Service
```bash
# Set scaling limits
gcloud run services update voice-assistant-openai \
    --min-instances=1 \
    --max-instances=50 \
    --region=us-central1
```

## 🔒 Security for Production

### 1. Environment Variables via Secret Manager
```bash
# Store secrets securely
echo -n "your_api_key" | gcloud secrets create openai-api-key --data-file=-

# Reference in Cloud Run
gcloud run services update voice-assistant-openai \
    --set-env-vars "OPENAI_API_KEY=$(gcloud secrets versions access latest --secret=openai-api-key)" \
    --region=us-central1
```

### 2. Authentication (Optional)
```bash
# Deploy with authentication required
gcloud run deploy voice-assistant-openai \
    --source . \
    --no-allow-unauthenticated \
    --region=us-central1
```

### 3. Custom Domain with SSL
```bash
# Map custom domain (SSL is automatic)
gcloud run domain-mappings create \
    --service voice-assistant-openai \
    --domain your-domain.com \
    --region us-central1
```

## 🎯 Production Checklist

- [ ] Google Cloud project created and configured
- [ ] Required APIs enabled (Cloud Run, Cloud Build)
- [ ] Environment variables configured
- [ ] Service deployed successfully
- [ ] Live URL obtained and tested
- [ ] Health check endpoint responding
- [ ] SSL certificate active (automatic)
- [ ] Custom domain configured (optional)
- [ ] Monitoring and logging set up
- [ ] Security policies reviewed

## 📞 Getting Support

If you encounter issues:

1. **Check deployment logs**:
   ```bash
   gcloud logs tail projects/YOUR_PROJECT_ID/logs/cloudbuild.googleapis.com
   ```

2. **Verify service health**:
   ```bash
   curl https://your-url.run.app/health
   ```

3. **Review configuration**:
   ```bash
   gcloud run services describe voice-assistant-openai --region=us-central1
   ```

## 🚀 Go Live Commands Summary

```bash
# Complete deployment workflow
git clone https://github.com/your-username/voice-assistant-openai.git
cd voice-assistant-openai

# Configure environment
cp .env.example .env
# Edit .env with your values

# Deploy to get live URL
./scripts/deploy.sh

# Your service is now live! URL will be displayed after deployment.
```

Your Voice Assistant OpenAI will be accessible worldwide at the provided Google Cloud Run URL!