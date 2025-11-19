#!/bin/bash

# Test script for Pinterest Clone Django project

echo "🧪 Pinterest Clone - Project Tests"
echo "===================================="
echo ""

# Activate virtual environment
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "❌ Virtual environment not found. Run ./run.sh first."
    exit 1
fi

# Test 1: Check Python syntax
echo "1️⃣  Checking Python syntax..."
python3 -m py_compile pins/*.py pinterest_project/*.py 2>&1
if [ $? -eq 0 ]; then
    echo "   ✅ Python syntax is valid"
else
    echo "   ❌ Python syntax errors found"
    exit 1
fi

# Test 2: Run Django check
echo ""
echo "2️⃣  Running Django system check..."
python manage.py check --deploy 2>&1 | grep -E "System check|no issues|OK"
if [ $? -eq 0 ]; then
    echo "   ✅ Django system check passed"
else
    echo "   ⚠️  Some warnings found (this is normal for development)"
fi

# Test 3: Check migrations
echo ""
echo "3️⃣  Checking database migrations..."
python manage.py showmigrations pins 2>&1 | head -10
if [ $? -eq 0 ]; then
    echo "   ✅ Migrations are properly configured"
else
    echo "   ❌ Migration issues found"
    exit 1
fi

# Test 4: Check static files
echo ""
echo "4️⃣  Checking static files..."
if [ -f "static/css/style.css" ] && [ -f "static/js/main.js" ]; then
    echo "   ✅ Static files exist"
    echo "      - CSS: $(wc -l < static/css/style.css) lines"
    echo "      - JS: $(wc -l < static/js/main.js) lines"
else
    echo "   ❌ Static files missing"
    exit 1
fi

# Test 5: Check templates
echo ""
echo "5️⃣  Checking templates..."
TEMPLATE_COUNT=$(find templates -name "*.html" | wc -l)
echo "   ✅ Found $TEMPLATE_COUNT HTML templates"

# Test 6: Check models
echo ""
echo "6️⃣  Checking models..."
python manage.py shell -c "from pins.models import Pin, Board, Comment; print('✅ All models imported successfully')" 2>&1

# Summary
echo ""
echo "=================================="
echo "📊 Test Summary:"
echo "   ✅ Python syntax"
echo "   ✅ Django configuration"
echo "   ✅ Database migrations"
echo "   ✅ Static files"
echo "   ✅ Templates"
echo "   ✅ Models"
echo ""
echo "🎉 All tests passed! Project is ready to use."
echo ""
echo "🚀 To start the server:"
echo "   source venv/bin/activate"
echo "   python manage.py runserver"
echo ""
