#!/bin/bash
CONTAINER_ID=$1

if [ -z "$CONTAINER_ID" ]; then
  echo "Usage: ./install.sh <container_id_or_name>"
  echo "Example: ./install.sh postgresql"
  exit 1
fi

echo "Installing pgvector to container $CONTAINER_ID..."

# Check if docker command exists
if ! command -v docker &> /dev/null; then
    echo "Error: docker command not found."
    exit 1
fi

# 1. Copy .so file to /opt/bitnami/postgresql/lib/
echo "Copying vector.so to /opt/bitnami/postgresql/lib/..."
docker cp files/vector.so "$CONTAINER_ID":/opt/bitnami/postgresql/lib/

# 2. Copy extension files to /opt/bitnami/postgresql/share/extension/
echo "Copying extension files to /opt/bitnami/postgresql/share/extension/..."
# We use a loop to ensure we copy files directly into the target directory
for f in files/*.sql files/*.control; do
    if [ -f "$f" ]; then
        docker cp "$f" "$CONTAINER_ID":/opt/bitnami/postgresql/share/extension/
    fi
done

echo "---------------------------------------------------"
echo "Installation complete!"
echo "Now please restart your database container (optional but recommended):"
echo "  docker restart $CONTAINER_ID"
echo ""
echo "Then log in to your database and run:"
echo "  CREATE EXTENSION vector;"
echo "---------------------------------------------------"
