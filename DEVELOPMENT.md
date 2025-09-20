# Development Workflow Best Practices

This document outlines best practices for maintaining your voice assistant repository when working between your local machine and Google Cloud Shell.

## 🏗️ Repository Structure

```
voice-assistant-openai/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile            # Docker configuration
├── docker-compose.yml    # Local development setup
├── .env.example          # Environment template
├── .env                  # Your environment variables (not in git)
├── .gitignore            # Git ignore rules
├── setup.sh              # Local setup script
├── scripts/
│   ├── gcloud-setup.sh   # Google Cloud Shell setup
│   ├── deploy.sh         # Deployment script
│   └── git-sync.sh       # Git workflow helper
├── static/               # Web assets
├── templates/            # HTML templates
├── tests/                # Test files
├── logs/                 # Application logs (not in git)
└── uploads/              # User uploads (not in git)
```

## 🔄 Git Workflow Best Practices

### 1. Branch Strategy
- `main` branch: Production-ready code
- `develop` branch: Integration branch for features
- Feature branches: `feature/description`
- Hotfix branches: `hotfix/issue-description`

### 2. Daily Workflow

#### On Your Local Machine:
```bash
# Start of day - sync with remote
./scripts/git-sync.sh sync

# Create feature branch
git checkout -b feature/new-functionality

# Work on your changes...
# When ready to commit
./scripts/git-sync.sh quick-commit "Add new functionality"

# Push feature branch
git push origin feature/new-functionality
```

#### In Google Cloud Shell:
```bash
# Clone or pull latest changes
git clone https://github.com/grogngy/voice-assistant-openai.git
cd voice-assistant-openai

# Or if already cloned
git pull origin main

# Set up environment
./scripts/gcloud-setup.sh

# Make adjustments for cloud environment
# Test changes...

# Commit cloud-specific adjustments
./scripts/git-sync.sh quick-commit "Cloud environment adjustments"
```

### 3. Environment Synchronization

#### Keep environments consistent:
1. **Use .env.example as template**
   ```bash
   cp .env.example .env
   # Edit .env with environment-specific values
   ```

2. **Version control configuration changes**
   - Update .env.example when adding new environment variables
   - Document environment differences in README

3. **Use Docker for consistency**
   ```bash
   # Local development
   docker-compose up

   # Cloud deployment
   ./scripts/deploy.sh
   ```

## ☁️ Google Cloud Shell Best Practices

### 1. First-Time Setup
```bash
# Clone repository
git clone https://github.com/grogngy/voice-assistant-openai.git
cd voice-assistant-openai

# Run Cloud Shell setup
./scripts/gcloud-setup.sh

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### 2. Working in Cloud Shell
```bash
# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Access via Web Preview on port 8080
```

### 3. Cloud Shell Limitations & Solutions

#### Storage Persistence:
- Cloud Shell storage persists in `/home/username`
- Clone repository to home directory: `~/voice-assistant-openai`
- Use `tmux` for persistent sessions

#### Environment Variables:
```bash
# Store sensitive variables in Cloud Shell
echo 'export OPENAI_API_KEY="your-key"' >> ~/.bashrc
source ~/.bashrc
```

#### Port Access:
```bash
# Use Web Preview for testing
# Access: https://8080-dot-PROJECT_ID.cloudshell.dev
```

## 🚀 Deployment Workflow

### 1. Development to Staging
```bash
# On local machine
git checkout develop
git merge feature/your-feature
git push origin develop

# In Cloud Shell
git checkout develop
git pull origin develop
./scripts/deploy.sh staging
```

### 2. Staging to Production
```bash
# After testing in staging
git checkout main
git merge develop
git push origin main

# Deploy to production
./scripts/deploy.sh production
```

## 🔧 Configuration Management

### 1. Environment-Specific Settings

#### Local Development (.env):
```
FLASK_ENV=development
FLASK_DEBUG=True
HOST=localhost
PORT=5000
```

#### Google Cloud Shell (.env):
```
FLASK_ENV=development
FLASK_DEBUG=True
HOST=0.0.0.0
PORT=8080
```

#### Production (.env):
```
FLASK_ENV=production
FLASK_DEBUG=False
HOST=0.0.0.0
PORT=8080
```

### 2. Secrets Management
- Use Google Secret Manager for production secrets
- Never commit API keys or sensitive data
- Use .env files for development only

## 📊 Monitoring & Maintenance

### 1. Regular Sync Schedule
```bash
# Daily sync routine
./scripts/git-sync.sh status    # Check status
./scripts/git-sync.sh sync      # Sync changes
```

### 2. Dependency Updates
```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt
pip freeze > requirements.txt

# Test updated dependencies
pip install -r requirements.txt
python -m pytest tests/
```

### 3. Cleanup Tasks
```bash
# Clean Docker images
docker system prune

# Clean Python cache
find . -type d -name "__pycache__" -delete

# Clean logs (keep last 7 days)
find logs/ -name "*.log" -mtime +7 -delete
```

## 🛠️ Troubleshooting

### Common Issues:

#### 1. Merge Conflicts
```bash
# Resolve conflicts manually, then:
git add .
git commit -m "Resolve merge conflicts"
git push origin your-branch
```

#### 2. Environment Differences
```bash
# Compare environments
diff .env.example .env

# Reset environment
rm .env
cp .env.example .env
# Reconfigure
```

#### 3. Cloud Shell Disconnection
```bash
# Use tmux for persistent sessions
tmux new-session -d -s voice-assistant
tmux attach-session -t voice-assistant
```

#### 4. Port Conflicts
```bash
# Kill processes on port
sudo lsof -ti:8080 | xargs sudo kill -9

# Use different port
export PORT=8081
python app.py
```

## 📋 Pre-Deployment Checklist

- [ ] All tests pass locally
- [ ] Environment variables configured
- [ ] Dependencies updated in requirements.txt
- [ ] Docker build succeeds
- [ ] Security scan passed
- [ ] Documentation updated
- [ ] Backup created
- [ ] Monitoring configured

## 🔗 Quick Commands

```bash
# Setup
./setup.sh                          # Local setup
./scripts/gcloud-setup.sh           # Cloud Shell setup

# Development
./scripts/git-sync.sh status        # Check repository status
./scripts/git-sync.sh sync          # Sync with remote
./scripts/git-sync.sh quick-commit "message"  # Quick commit

# Deployment
./scripts/deploy.sh                 # Deploy to Cloud Run

# Docker
docker-compose up                   # Local development
docker-compose down                 # Stop local environment
```