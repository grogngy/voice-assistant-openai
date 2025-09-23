# 🎤 Voice Assistant OpenAI

A Flask app for real-time voice and text chat with OpenAI GPT, using Google Cloud TTS/STT. Features a modern web UI, Docker support, SSL, and .env config. Ready for deployment on Google Cloud Run. Ideal for building conversational AI assistants.

## ✨ Features

- 🎯 Real-time voice and text conversations with OpenAI GPT
- 🗣️ Google Cloud Speech-to-Text integration
- 🔊 Google Cloud Text-to-Speech with natural voices
- 🌐 Modern responsive web interface
- 🐳 Docker support for consistent development
- ☁️ Google Cloud Run deployment ready
- 🔒 SSL/TLS support for secure communications
- ⚙️ Environment-based configuration
- 📱 Mobile-friendly design

## 🚀 Quick Start

### 🌐 Deploy to Google Cloud (Get Live URL)

**Get your Voice Assistant live in 2 minutes:**

```bash
git clone https://github.com/grogngy/voice-assistant-openai.git
cd voice-assistant-openai
cp .env.example .env
# Edit .env with your API keys
./scripts/deploy.sh
```

**Your live URL will be displayed after deployment!**

For detailed deployment instructions, see [LIVE_URL_GUIDE.md](LIVE_URL_GUIDE.md).

### Local Development

1. **Clone and Setup**
   ```bash
   git clone https://github.com/grogngy/voice-assistant-openai.git
   cd voice-assistant-openai
   ./setup.sh
   ```

2. **Configure Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

3. **Run the Application**
   ```bash
   source venv/bin/activate
   python app.py
   ```

### Google Cloud Shell

1. **Setup in Cloud Shell**
   ```bash
   git clone https://github.com/grogngy/voice-assistant-openai.git
   cd voice-assistant-openai
   ./scripts/gcloud-setup.sh
   ```

2. **Configure for Cloud**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   source venv/bin/activate
   python app.py
   ```

3. **Access via Web Preview** (Port 8080)

## 📋 Prerequisites

- Python 3.11+
- OpenAI API key
- Google Cloud Project with:
  - Speech-to-Text API enabled
  - Text-to-Speech API enabled
  - Service account with appropriate permissions

## ⚙️ Configuration

### Required Environment Variables

```bash
# OpenAI
OPENAI_API_KEY=your_openai_api_key

# Google Cloud
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account.json

# Application
FLASK_ENV=development
SECRET_KEY=your-secret-key
```

See `.env.example` for complete configuration options.

## 🐳 Docker Development

```bash
# Local development with Docker
docker-compose up

# Production build
docker build -t voice-assistant-openai .
docker run -p 8080:8080 --env-file .env voice-assistant-openai
```

## ☁️ Google Cloud Deployment

### 🎯 Get Live URL (Production Ready)
```bash
# One-command deployment to get live URL
./scripts/deploy.sh

# Get URL of existing deployment
./scripts/get-url.sh
```

**📖 Complete deployment guide: [LIVE_URL_GUIDE.md](LIVE_URL_GUIDE.md)**

### Manual Deployment
```bash
# Deploy to Cloud Run
gcloud run deploy voice-assistant-openai \
    --source . \
    --platform managed \
    --region us-central1 \
    --allow-unauthenticated
```

## 🔄 Development Workflow Best Practices

This repository includes comprehensive tools and documentation for managing development workflow between local machines and Google Cloud Shell.

### Key Scripts

- `./setup.sh` - Local environment setup
- `./scripts/deploy.sh` - Deploy to Google Cloud and get live URL
- `./scripts/get-url.sh` - Get the live URL of deployed service
- `./scripts/status.sh` - Check service health and status
- `./scripts/gcloud-setup.sh` - Google Cloud Shell setup
- `./scripts/git-sync.sh` - Git workflow helper

### Workflow Commands

```bash
# Check repository status
./scripts/git-sync.sh status

# Sync with remote repository
./scripts/git-sync.sh sync

# Quick commit and push
./scripts/git-sync.sh quick-commit "Your commit message"

# Deploy to production
./scripts/deploy.sh
```

📖 **For detailed workflow documentation, see [DEVELOPMENT.md](DEVELOPMENT.md)**  
🚀 **For deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)**

## 📁 Project Structure

```
voice-assistant-openai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Local development setup
├── .env.example          # Environment template
├── setup.sh              # Local setup script
├── scripts/              # Utility scripts
│   ├── gcloud-setup.sh   # Google Cloud Shell setup
│   ├── deploy.sh         # Deployment script
│   └── git-sync.sh       # Git workflow helper
├── static/               # Web assets
├── templates/            # HTML templates
├── tests/               # Test files
└── DEVELOPMENT.md        # Detailed workflow guide
```

## 🛠️ Development Tools

### Code Quality
```bash
# Format code
black .

# Lint code
flake8 .

# Sort imports
isort .

# Run tests
pytest
```

### Git Workflow
```bash
# Daily sync routine
./scripts/git-sync.sh sync

# Quick development cycle
./scripts/git-sync.sh quick-commit "Feature update"
```

## 🔒 Security Best Practices

- ✅ Never commit API keys or secrets
- ✅ Use environment variables for configuration
- ✅ Enable SSL/TLS for production
- ✅ Regularly update dependencies
- ✅ Use Google Secret Manager for production secrets
- ✅ Implement proper authentication for production

## 📊 Monitoring & Logging

- Application logs in `logs/` directory
- Google Cloud Logging integration
- Health check endpoint at `/health`
- Performance monitoring with Cloud Monitoring

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes and test thoroughly
4. Commit your changes: `./scripts/git-sync.sh quick-commit "Add new feature"`
5. Push to your fork: `git push origin feature/new-feature`
6. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- 📖 Check [DEVELOPMENT.md](DEVELOPMENT.md) for detailed documentation
- 🐛 Report issues on GitHub
- 💬 Join discussions in GitHub Discussions

## 🙏 Acknowledgments

- OpenAI for GPT API
- Google Cloud for Speech and TTS services
- Flask community for the excellent framework
