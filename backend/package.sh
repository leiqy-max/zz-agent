#!/bin/bash
set -e

# Activate venv
source venv39/bin/activate

# Build binary
echo "Building binary with PyInstaller..."
pyinstaller --clean ops-agent-dyn.spec

# Static linking
echo "Linking statically with StaticX..."
staticx dist/ops-agent-dyn ops-agent-static

# Prepare release folder
echo "Packaging..."
mkdir -p release/final_package
cp ops-agent-static release/final_package/ops-agent
cp config.yaml release/final_package/
cp release/init.sql release/final_package/
cp -r release/pgvector_ext release/final_package/

# Zip
cd release/final_package
zip -r ../ops-agent-linux-x64.zip .
cd ../..

echo "Done! Package at backend/release/ops-agent-linux-x64.zip"
