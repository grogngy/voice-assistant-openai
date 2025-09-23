#!/bin/bash

# Status Check Script for Voice Assistant OpenAI
# Checks the health and status of the deployed service

set -e

echo "🔍 Checking Voice Assistant Status..."

# Check if deployment URL file exists
if [ -f ".deployment-url" ]; then
    SERVICE_URL=$(cat .deployment-url)
    echo "📋 Found saved URL: $SERVICE_URL"
else
    echo "⚠️  No saved URL found. Getting from Google Cloud..."
    
    # Check if gcloud is configured
    if ! gcloud config get-value project > /dev/null 2>&1; then
        echo "❌ Please run 'gcloud init' to configure your Google Cloud project"
        exit 1
    fi
    
    PROJECT_ID=$(gcloud config get-value project)
    SERVICE_NAME="voice-assistant-openai"
    REGION="us-central1"
    
    # Get service URL
    SERVICE_URL=$(gcloud run services describe $SERVICE_NAME --region=$REGION --format="value(status.url)" 2>/dev/null || echo "")
    
    if [ -z "$SERVICE_URL" ]; then
        echo "❌ Service not found. Deploy first using: ./scripts/deploy.sh"
        exit 1
    fi
    
    # Save URL for next time
    echo "$SERVICE_URL" > .deployment-url
    echo "💾 URL saved to .deployment-url"
fi

echo ""
echo "🧪 Running Health Checks..."

# Check main application
echo -n "📱 Main Application: "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Online (HTTP $HTTP_CODE)"
    MAIN_STATUS="OK"
else
    echo "❌ Issues (HTTP $HTTP_CODE)"
    MAIN_STATUS="ERROR"
fi

# Check health endpoint
echo -n "🏥 Health Endpoint: "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL/health" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Healthy (HTTP $HTTP_CODE)"
    HEALTH_STATUS="OK"
    # Get health details
    HEALTH_RESPONSE=$(curl -s "$SERVICE_URL/health" 2>/dev/null || echo "{}")
    echo "   Response: $HEALTH_RESPONSE"
else
    echo "❌ Unhealthy (HTTP $HTTP_CODE)"
    HEALTH_STATUS="ERROR"
fi

# Check config endpoint
echo -n "⚙️  Config Endpoint: "
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" "$SERVICE_URL/config" 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo "✅ Available (HTTP $HTTP_CODE)"
    CONFIG_STATUS="OK"
else
    echo "❌ Issues (HTTP $HTTP_CODE)"
    CONFIG_STATUS="ERROR"
fi

# Check SSL certificate
echo -n "🔒 SSL Certificate: "
SSL_INFO=$(echo | openssl s_client -servername "$(echo $SERVICE_URL | sed 's|https://||' | sed 's|/.*||')" -connect "$(echo $SERVICE_URL | sed 's|https://||' | sed 's|/.*||'):443" 2>/dev/null | openssl x509 -noout -dates 2>/dev/null || echo "")
if [ -n "$SSL_INFO" ]; then
    echo "✅ Valid"
    echo "   $SSL_INFO"
    SSL_STATUS="OK"
else
    echo "⚠️  Could not verify"
    SSL_STATUS="UNKNOWN"
fi

echo ""
echo "📊 Status Summary"
echo "=================="
echo "🌐 URL: $SERVICE_URL"
echo "📱 Main App: $MAIN_STATUS"
echo "🏥 Health: $HEALTH_STATUS"
echo "⚙️  Config: $CONFIG_STATUS"
echo "🔒 SSL: $SSL_STATUS"

if [ "$MAIN_STATUS" = "OK" ] && [ "$HEALTH_STATUS" = "OK" ]; then
    echo ""
    echo "🎉 Your Voice Assistant is LIVE and working!"
    echo "🔗 Share this URL: $SERVICE_URL"
else
    echo ""
    echo "⚠️  Your service has some issues. Check the logs:"
    echo "   gcloud logs tail projects/$(gcloud config get-value project)/logs/run.googleapis.com"
fi

echo ""
echo "🛠️  Management Commands:"
echo "   Update: ./scripts/deploy.sh"
echo "   Logs: gcloud logs tail projects/$(gcloud config get-value project)/logs/run.googleapis.com"
echo "   Restart: gcloud run services update voice-assistant-openai --region=us-central1"