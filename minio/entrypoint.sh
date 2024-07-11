#!/bin/bash

# Function to check MinIO server health
check_minio_health() {
    HEALTHCHECK_URL="http://localhost:9000/minio/health/ready"
    HEALTHCHECK_TIMEOUT=60  # Timeout in seconds
    HEALTHCHECK_INTERVAL=5  # Interval between retries in seconds

    echo "Checking MinIO server health..."

    # Try to fetch health status until timeout
    for (( i=0; i<HEALTHCHECK_TIMEOUT; i+=HEALTHCHECK_INTERVAL )); do
        HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTHCHECK_URL)
        if [ $HEALTH_STATUS -eq 200 ]; then
            echo "MinIO server is ready."
            return 0
        else
            echo "MinIO server not ready yet, retrying in $HEALTHCHECK_INTERVAL seconds..."
            sleep $HEALTHCHECK_INTERVAL
        fi
    done

    echo "MinIO server did not become ready within the timeout period."
    return 1
}

# Start MinIO server in the background
/usr/bin/minio server /data --address :9000 --console-address :9001 &

# Wait for MinIO server to start and become ready
if ! check_minio_health; then
    echo "Exiting due to MinIO server not being ready."
    exit 1
fi

# Set MinIO alias with credentials (optional)
mc alias set myminio http://localhost:9000 minioroot miniopassword

# Create MinIO bucket using mc
mc mb myminio/olympicweightliftingbucket

# Check if bucket creation was successful
if [ $? -eq 0 ]; then
    echo "Bucket 'olympicweightliftingbucket' created successfully."
else
    echo "Failed to create bucket 'olympicweightliftingbucket'."
fi

# Keep container running (if needed)
tail -f /dev/null
