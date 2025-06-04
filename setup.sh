#!/bin/bash

echo "🚀 Setting up KV Board Deck Parser MVP..."

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file..."
    echo "OPENAI_API_KEY=your-api-key-here" > .env
    echo "⚠️  Please edit .env and add your OpenAI API key!"
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env and add your OpenAI API key"
echo "2. Run: source venv/bin/activate"
echo "3. Run: streamlit run kv_mvp.py"
echo ""
echo "🌟 Your app will open at http://localhost:8501" 