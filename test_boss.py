#!/usr/bin/env python
"""
Тестовый скрипт для проверки Ultimate Boss Agent
"""
import asyncio
import httpx
import sys

async def test_health():
    """Проверка health endpoint"""
    print("🏥 Testing health endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/health")
            response.raise_for_status()
            data = response.json()
            print(f"  ✓ Health check passed: {data}")
            return True
        except Exception as e:
            print(f"  ✗ Health check failed: {e}")
            return False

async def test_memory_stats():
    """Проверка статистики памяти"""
    print("\n📊 Testing memory stats...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get("http://localhost:8000/memory/stats")
            response.raise_for_status()
            data = response.json()
            print(f"  ✓ Memory stats retrieved:")
            print(f"    • Total memories: {data['total_memories']}")
            print(f"    • Total solutions: {data['total_solutions']}")
            print(f"    • Active delegations: {data['active_delegations']}")
            return True
        except Exception as e:
            print(f"  ✗ Memory stats failed: {e}")
            return False

async def test_teach():
    """Проверка обучения"""
    print("\n🎓 Testing teach endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/teach",
                json={"lesson": "Test lesson: Always write unit tests"}
            )
            response.raise_for_status()
            data = response.json()
            print(f"  ✓ Teach successful: {data}")
            return True
        except Exception as e:
            print(f"  ✗ Teach failed: {e}")
            return False

async def test_demonstrate():
    """Проверка демонстрации"""
    print("\n🎯 Testing demonstrate endpoint...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                "http://localhost:8000/demonstrate",
                json={
                    "task": "Test task",
                    "solution": "Test solution steps"
                }
            )
            response.raise_for_status()
            data = response.json()
            print(f"  ✓ Demonstrate successful: {data}")
            return True
        except Exception as e:
            print(f"  ✗ Demonstrate failed: {e}")
            return False

async def test_memory_search():
    """Проверка поиска в памяти"""
    print("\n🔍 Testing memory search...")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                "http://localhost:8000/memory/search",
                params={"query": "test"}
            )
            response.raise_for_status()
            data = response.json()
            print(f"  ✓ Search successful: Found {len(data.get('results', []))} results")
            return True
        except Exception as e:
            print(f"  ✗ Search failed: {e}")
            return False

async def test_process_task():
    """Проверка обработки задачи (требует настроенные API ключи)"""
    print("\n🚀 Testing task processing...")
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            response = await client.post(
                "http://localhost:8000/process",
                json={
                    "task": "Test task: Echo this message",
                    "mode": "boss"
                }
            )
            response.raise_for_status()
            data = response.json()
            print(f"  ✓ Task processing successful:")
            print(f"    • Agent ID: {data.get('agent_id')}")
            print(f"    • Status: {data.get('status')}")
            print(f"    • Used memory: {data.get('used_memory')}")
            if data.get('web_url'):
                print(f"    • Web URL: {data.get('web_url')}")
            return True
        except httpx.HTTPStatusError as e:
            print(f"  ⚠️  Task processing failed: {e}")
            print(f"  This is expected if Codegen API keys are not configured")
            return None
        except Exception as e:
            print(f"  ✗ Task processing error: {e}")
            return False

async def run_all_tests():
    """Запускает все тесты"""
    print("="*60)
    print("🧪 Ultimate Boss Agent - Test Suite")
    print("="*60)
    
    results = []
    
    # Базовые тесты
    results.append(("Health Check", await test_health()))
    results.append(("Memory Stats", await test_memory_stats()))
    results.append(("Teach", await test_teach()))
    results.append(("Demonstrate", await test_demonstrate()))
    results.append(("Memory Search", await test_memory_search()))
    
    # Тест обработки задачи (может не пройти без API ключей)
    task_result = await test_process_task()
    if task_result is not None:
        results.append(("Task Processing", task_result))
    
    # Итоги
    print("\n" + "="*60)
    print("📋 Test Results:")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {name}")
    
    print(f"\n📊 Score: {passed}/{total} tests passed")
    
    if passed == total:
        print("✅ All tests passed!")
        return 0
    elif passed >= total * 0.8:
        print("⚠️  Most tests passed, but some failed")
        return 1
    else:
        print("❌ Many tests failed")
        return 2

if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)

