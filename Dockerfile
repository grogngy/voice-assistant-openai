FROM python:3.10

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8080 for Cloud Run
EXPOSE 8080

# Use gunicorn for production
CMD ["gunicorn", "-b", "0.0.0.0:8080", "server:app"]