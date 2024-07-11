FROM minio/minio:RELEASE.2024-06-22T05-26-45Z

# Set environment variables for MinIO
ENV MINIO_ROOT_USER=minioroot
ENV MINIO_ROOT_PASSWORD=miniopassword

# Expose MinIO ports (default HTTP and optional HTTPS)
EXPOSE 9000 9001

# Copy entrypoint script into the container
COPY entrypoint.sh /entrypoint.sh

# Make entrypoint script executable
RUN chmod +x /entrypoint.sh

# Set the entrypoint command to execute the script
ENTRYPOINT ["/entrypoint.sh"]

