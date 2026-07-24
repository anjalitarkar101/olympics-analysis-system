#!/bin/bash

echo "=========================================="
echo "🏅 Olympics Analysis System - Setup"
echo "=========================================="

# Create directories
echo "📁 Creating directories..."
mkdir -p data
mkdir -p images
mkdir -p saved_visualizations

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

echo ""
echo "=========================================="
echo "✅ Setup complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Place CSV files in 'data/' folder:"
echo "2. streamlit run app.py"
echo ""