#!/bin/bash

# Deployment Script for Google Cloud Run
# Deploys the voice assistant to Google Cloud Run

set -e

echo "🚀 Deploying Voice Assistant to Google Cloud Run..."

# Check if gcloud is configured
if ! gcloud config get-value project > /dev/null 2>&1; then
    echo "❌ Please run 'gcloud init' to configure your Google Cloud project"
    exit 1
fi

PROJECT_ID=$(gcloud config get-value project)
echo "📋 Project ID: $PROJECT_ID"

# Set variables
SERVICE_NAME="voice-assistant-openai"
REGION="us-central1"
IMAGE_NAME="gcr.io/$PROJECT_ID/$SERVICE_NAME"

# Build and push Docker image using Cloud Build (more reliable)
echo "🏗️  Building with Cloud Build..."
gcloud builds submit --tag $IMAGE_NAME

echo "☁️ Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
    --image $IMAGE_NAME \
    --platform managed \
    --region $REGION \
    --allow-unauthenticated \
    --port 8080 \
    --memory 1Gi \
    --cpu 1 \
    --max-instances 10 \
    --set-env-vars "FLASK_ENV=production" \
    --set-env-vars "GOOGLE_CLOUD_PROJECT=$PROJECT_ID"

# Get service URL
echo "🔍 Retrieving service URL..."
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

if [ -z "$SERVICE_URL" ]; then
    echo "❌ Could not retrieve service URL"
    exit 1
fi

echo ""
echo "🎉 Deployment Complete!"
echo "================================="
echo "🌐 Your Voice Assistant is now LIVE!"
echo "🔗 Live URL: $SERVICE_URL"
echo "================================="
echo ""
echo "🚀 Quick Start:"
echo "   1. Open in browser: $SERVICE_URL"
echo "   2. Test health: $SERVICE_URL/health"
echo "   3. View config: $SERVICE_URL/config"
echo ""
echo "🔧 Next Steps:"
echo "   - Set environment variables: gcloud run services update $SERVICE_NAME --set-env-vars 'KEY=VALUE' --region=$REGION"
echo "   - Configure custom domain: gcloud run domain-mappings create --service=$SERVICE_NAME --domain=yourdomain.com --region=$REGION"
echo "   - Monitor logs: gcloud logs tail projects/$PROJECT_ID/logs/run.googleapis.com"
echo ""
echo "💾 URL saved to .deployment-url for easy access"
echo "$SERVICE_URL" > .deployment-url

# Test the deployment
echo "🧪 Testing deployment..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" $SERVICE_URL/health)
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Health check passed - Service is healthy!"
else
    echo "⚠️  Health check returned status: $HTTP_CODE"
fi

echo ""
echo "🎯 Your Voice Assistant OpenAI is ready!"
echo "Share this URL to go live: $SERVICE_URL"