#!/bin/bash
# Quick start script for Ultimate Boss Agent

set -e

echo "🤖 Ultimate Boss Agent - Quick Start"
echo "===================================="

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo "📝 Creating .env from .env.example..."
    cp .env.example .env
    echo "✏️  Please edit .env and add your API keys:"
    echo "   - CODEGEN_ORG_ID"
    echo "   - CODEGEN_API_TOKEN"
    echo "   - OPENAI_API_KEY"
    echo ""
    read -p "Press Enter after you've configured .env..."
fi

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ docker-compose not found. Please install Docker Compose."
    exit 1
fi

echo ""
echo "🏗️  Building Docker image..."
docker-compose build

echo ""
echo "🚀 Starting services..."
docker-compose up -d

echo ""
echo "⏳ Waiting for services to be ready..."
sleep 5

echo ""
echo "🏥 Checking health..."
max_retries=30
counter=0
while [ $counter -lt $max_retries ]; do
    if curl -s http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Service is healthy!"
        break
    fi
    counter=$((counter + 1))
    echo "   Attempt $counter/$max_retries..."
    sleep 2
done

if [ $counter -eq $max_retries ]; then
    echo "❌ Service failed to become healthy"
    echo "📋 Checking logs..."
    docker-compose logs --tail=50
    exit 1
fi

echo ""
echo "📚 Initializing knowledge base..."
docker-compose exec ultimate-boss-memory python init_boss_knowledge.py

echo ""
echo "🧪 Running tests..."
docker-compose exec ultimate-boss-memory python test_boss.py

echo ""
echo "✅ Ultimate Boss Agent is ready!"
echo ""
echo "📋 Useful commands:"
echo "   • View logs: docker-compose logs -f"
echo "   • Stop: docker-compose down"
echo "   • Restart: docker-compose restart"
echo ""
echo "🌐 API endpoints:"
echo "   • Health: http://localhost:8000/health"
echo "   • Process task: POST http://localhost:8000/process"
echo "   • Teach: POST http://localhost:8000/teach"
echo "   • Memory stats: GET http://localhost:8000/memory/stats"
echo ""
echo "📖 Example curl commands:"
echo '   curl http://localhost:8000/health'
echo '   curl http://localhost:8000/memory/stats'
echo '   curl -X POST http://localhost:8000/process \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"task": "Your task here", "mode": "boss"}'"'"
echo ""

