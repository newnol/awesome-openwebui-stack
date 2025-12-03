#!/bin/bash
# Helper script to test diagram_generator.py tool

# Activate virtual environment if it exists
if [ -d ".env" ]; then
    source .env/bin/activate
fi

# Create output directory if it doesn't exist
mkdir -p output

# Run the tool with test file
python3 tools/diagram_generator.py test_diagram.py \
    --output-dir "$(pwd)/output" \
    --format png \
    --filename test_result

echo ""
echo "✅ Check the output directory for test_result.png"

