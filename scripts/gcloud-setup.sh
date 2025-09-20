#!/bin/bash

# Google Cloud Shell Setup Script
# Optimized for Google Cloud Shell environment

set -e

echo "☁️ Setting up Voice Assistant OpenAI for Google Cloud Shell..."

# Update package lists
echo "📦 Updating package lists..."
sudo apt-get update

# Install required system packages
echo "🔧 Installing system dependencies..."
sudo apt-get install -y \
    python3-pip \
    python3-venv \
    portaudio19-dev \
    python3-dev \
    gcc \
    curl

# Set up Python virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install -r requirements.txt

# Set up Google Cloud SDK (usually pre-installed in Cloud Shell)
echo "☁️ Configuring Google Cloud SDK..."

# Check if gcloud is configured
if ! gcloud config get-value project > /dev/null 2>&1; then
    echo "⚠️ Please run 'gcloud init' to configure your Google Cloud project"
else
    PROJECT_ID=$(gcloud config get-value project)
    echo "✅ Current project: $PROJECT_ID"
fi

# Enable required APIs
echo "🔌 Enabling required Google Cloud APIs..."
gcloud services enable \
    speech.googleapis.com \
    texttospeech.googleapis.com \
    run.googleapis.com \
    cloudbuild.googleapis.com

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "⚙️ Creating .env file from template..."
    cp .env.example .env
    
    # Set project ID in .env
    if [ ! -z "$PROJECT_ID" ]; then
        sed -i "s/your-gcp-project-id/$PROJECT_ID/g" .env
    fi
    
    echo "📝 Please edit .env file with your API keys"
fi

# Create necessary directories
mkdir -p logs uploads audio_files

# Set up Cloud Shell port forwarding info
echo "🌐 Cloud Shell port forwarding setup:"
echo "When running the app, use Web Preview on port 8080"
echo "Or access via: https://8080-dot-$DEVSHELL_PROJECT_ID.cloudshell.dev"

echo "✅ Google Cloud Shell setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your OpenAI API key"
echo "2. Run 'source venv/bin/activate' to activate virtual environment"
echo "3. Run 'python app.py' to start the development server"
echo "4. Use Web Preview to access the application"