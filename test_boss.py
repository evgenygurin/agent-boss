#!/usr/bin/env python3
"""
Тестовый скрипт для проверки Ultimate Boss Agent
"""
import asyncio
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

BASE_URL = "http://localhost:8000"

async def test_simple_delegation():
    """Тест простого делегирования"""
    print("\n🧪 Test 1: Simple Delegation")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/process",
            json={
                "task": "Create a simple hello world Python script",
                "mode": "boss"
            },
            timeout=60.0
        )
        result = response.json()
        
        print(f"✓ Agent ID: {result['agent_id']}")
        print(f"✓ Status: {result['status']}")
        print(f"✓ Used Memory: {result['used_memory']}")
        print(f"✓ Web URL: {result.get('web_url', 'N/A')}")
    
    return result

async def test_teach_boss():
    """Тест обучения босса"""
    print("\n🧪 Test 2: Teaching Boss")
    print("=" * 50)
    
    lessons = [
        "Always add type hints to Python functions",
        "Use pytest for testing Python code",
        "Follow PEP 8 style guide"
    ]
    
    async with httpx.AsyncClient() as client:
        for lesson in lessons:
            response = await client.post(
                f"{BASE_URL}/teach",
                json={"lesson": lesson},
                timeout=30.0
            )
            result = response.json()
            print(f"✓ Taught: {lesson}")
    
    print(f"\n✅ Successfully taught {len(lessons)} lessons")

async def test_demonstrate_solution():
    """Тест демонстрации решения"""
    print("\n🧪 Test 3: Demonstrate Solution")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/demonstrate",
            json={
                "task": "Write Python unit tests",
                "solution": "1. Create test file\n2. Write test functions\n3. Use pytest fixtures\n4. Run with pytest"
            },
            timeout=30.0
        )
        result = response.json()
        
        print(f"✓ Status: {result['status']}")
        print(f"✓ Task: {result['task']}")

async def test_memory_search():
    """Тест поиска в памяти"""
    print("\n🧪 Test 4: Memory Search")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/memory/search",
            params={"query": "python"},
            timeout=30.0
        )
        result = response.json()
        
        print(f"✓ Mem0 results: {len(result['mem0'])} items")
        print(f"✓ Vector results: {len(result['vector'])} items")
        
        if result['mem0']:
            print(f"\nFirst Mem0 result:")
            print(f"  {result['mem0'][0][:100]}...")

async def test_memory_stats():
    """Тест статистики памяти"""
    print("\n🧪 Test 5: Memory Statistics")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/memory/stats",
            timeout=30.0
        )
        result = response.json()
        
        print(f"✓ Total memories: {result['total_memories']}")
        print(f"✓ Active delegations: {result['active_delegations']}")
        print(f"✓ Memory types:")
        for mem_type, count in result['memory_types'].items():
            print(f"    - {mem_type}: {count}")

async def test_team_delegation():
    """Тест делегирования через команду"""
    print("\n🧪 Test 6: Team Delegation")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/process",
            json={
                "task": "Complex task: Create a REST API with authentication and database",
                "mode": "team"
            },
            timeout=60.0
        )
        result = response.json()
        
        print(f"✓ Task: {result['task'][:50]}...")
        print(f"✓ Delegations created: {len(result['delegations'])}")
        
        for i, delegation in enumerate(result['delegations'], 1):
            print(f"\n  Delegation {i}:")
            print(f"    Agent ID: {delegation['agent_id']}")
            print(f"    Status: {delegation['status']}")

async def test_learning_mode():
    """Тест режима обучения"""
    print("\n🧪 Test 7: Learning Mode")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"{BASE_URL}/process",
            json={
                "task": "Create a function to validate email addresses",
                "mode": "learn"
            },
            timeout=60.0
        )
        result = response.json()
        
        print(f"✓ Agent ID: {result['agent_id']}")
        print(f"✓ Status: {result['status']}")
        print(f"✓ Used Memory: {result['used_memory']}")

async def run_all_tests():
    """Запускает все тесты"""
    print("\n" + "=" * 50)
    print("🚀 Ultimate Boss Agent - Test Suite")
    print("=" * 50)
    
    try:
        # Проверка доступности сервера
        async with httpx.AsyncClient() as client:
            try:
                await client.get(f"{BASE_URL}/memory/stats", timeout=5.0)
                print("✅ Server is running\n")
            except httpx.ConnectError:
                print("❌ Server is not running!")
                print("Please start the server with: python ultimate_boss_with_memory.py")
                return
        
        # Запуск тестов
        await test_teach_boss()
        await test_demonstrate_solution()
        await test_simple_delegation()
        await test_memory_search()
        await test_memory_stats()
        await test_team_delegation()
        await test_learning_mode()
        
        print("\n" + "=" * 50)
        print("✅ All tests completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(run_all_tests())
