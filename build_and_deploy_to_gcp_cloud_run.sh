# 1. Build and tag the image
docker build -t europe-west1-docker.pkg.dev/sandbox-459602/ws/bubblemaps-trending-api:latest .

# 2. Push the image to Artifact Registry
docker push europe-west1-docker.pkg.dev/sandbox-459602/ws/bubblemaps-trending-api:latest

# 3. Deploy to Cloud Run
gcloud run deploy bubblemaps-trending-api \
    --image europe-west1-docker.pkg.dev/sandbox-459602/ws/bubblemaps-trending-api:latest \
    --platform managed \
    --region europe-west1 \
    --allow-unauthenticated
