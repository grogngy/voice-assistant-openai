#!/bin/bash

# Get Live URL Script for Voice Assistant OpenAI
# Retrieves the current live URL of the deployed service

set -e

echo "🌐 Getting Voice Assistant Live URL..."

# Check if gcloud is configured
if ! gcloud config get-value project > /dev/null 2>&1; then
    echo "❌ Please run 'gcloud init' to configure your Google Cloud project"
    exit 1
fi

PROJECT_ID=$(gcloud config get-value project)
SERVICE_NAME="voice-assistant-openai"
REGION="us-central1"

echo "📋 Project ID: $PROJECT_ID"
echo "📋 Service Name: $SERVICE_NAME"
echo "📋 Region: $REGION"

# Check if service exists
if ! gcloud run services describe $SERVICE_NAME --region=$REGION >/dev/null 2>&1; then
    echo "❌ Service '$SERVICE_NAME' not found in region '$REGION'"
    echo "💡 Deploy the service first using: ./scripts/deploy.sh"
    exit 1
fi

# Get service URL
SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)")

if [ -z "$SERVICE_URL" ]; then
    echo "❌ Could not retrieve service URL"
    exit 1
fi

echo ""
echo "✅ Voice Assistant is live!"
echo "🌐 Live URL: $SERVICE_URL"
echo ""
echo "📝 Quick access commands:"
echo "   Open in browser: open $SERVICE_URL"
echo "   Copy to clipboard: echo '$SERVICE_URL' | pbcopy"
echo ""
echo "🔧 Management commands:"
echo "   View logs: gcloud logs tail projects/$PROJECT_ID/logs/run.googleapis.com"
echo "   Update service: ./scripts/deploy.sh"
echo "   Service status: gcloud run services describe $SERVICE_NAME --region=$REGION"
echo ""
echo "🔗 Direct links:"
echo "   Voice Assistant: $SERVICE_URL"
echo "   Health Check: $SERVICE_URL/health"
echo "   Configuration: $SERVICE_URL/config"

# Save URL to file for easy access
echo "$SERVICE_URL" > .deployment-url
echo "💾 URL saved to .deployment-url file"