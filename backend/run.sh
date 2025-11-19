#!/bin/bash

# Quick start script for Pinterest Clone Django project

echo "🎨 Pinterest Clone - Quick Start Script"
echo "========================================"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -q -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py migrate

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput > /dev/null 2>&1

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Create superuser: python manage.py createsuperuser"
echo "   2. Start server: python manage.py runserver"
echo "   3. Open browser: http://127.0.0.1:8000"
echo "   4. Admin panel: http://127.0.0.1:8000/admin"
echo ""
echo "🚀 To start the server now, run:"
echo "   python manage.py runserver"
echo ""
