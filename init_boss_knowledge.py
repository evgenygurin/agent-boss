#!/usr/bin/env python
"""
Инициализация базы знаний Ultimate Boss Agent
"""
import asyncio
import os
from dotenv import load_dotenv
from ultimate_boss_with_memory import UltimateMemoryOrchestrator

load_dotenv()

async def initialize():
    """Инициализирует базу знаний босса"""
    
    print("🚀 Initializing Ultimate Boss Knowledge Base...")
    
    orchestrator = UltimateMemoryOrchestrator(
        codegen_org_id=os.getenv("CODEGEN_ORG_ID", ""),
        codegen_token=os.getenv("CODEGEN_API_TOKEN", ""),
        openai_key=os.getenv("OPENAI_API_KEY", "")
    )
    
    # Обучаем базовым паттернам
    print("\n📚 Teaching basic patterns...")
    lessons = [
        "Always check CI/CD status before merging PRs",
        "Use Linear sub-issues for complex tasks",
        "Monitor Sentry for production errors",
        "Create comprehensive tests for all features",
        "Document all API changes",
        "Use semantic commit messages",
        "Review security implications before deployment",
        "Keep dependencies up to date",
        "Follow code review best practices",
        "Maintain clear commit history"
    ]
    
    for i, lesson in enumerate(lessons, 1):
        await orchestrator.teach(lesson)
        print(f"  ✓ Lesson {i}/{len(lessons)}: {lesson}")
    
    # Демонстрируем успешные решения
    print("\n🎯 Demonstrating successful solutions...")
    demonstrations = [
        (
            "Fix failing tests",
            "1. Run tests locally\n2. Identify failure root cause\n3. Fix code\n4. Verify fix\n5. Commit and push"
        ),
        (
            "Deploy to production",
            "1. Check staging environment\n2. Run smoke tests\n3. Deploy with monitoring\n4. Verify deployment\n5. Monitor for issues"
        ),
        (
            "Code review",
            "1. Check logic correctness\n2. Review security implications\n3. Verify test coverage\n4. Assess performance\n5. Check documentation"
        ),
        (
            "Bug fix workflow",
            "1. Reproduce the bug\n2. Write failing test\n3. Fix the bug\n4. Verify test passes\n5. Check for regressions"
        ),
        (
            "Feature implementation",
            "1. Design and plan\n2. Break into subtasks\n3. Implement incrementally\n4. Test thoroughly\n5. Document and PR"
        ),
        (
            "Refactoring",
            "1. Identify code smell\n2. Write tests first\n3. Refactor incrementally\n4. Verify tests pass\n5. Document changes"
        ),
        (
            "Performance optimization",
            "1. Profile and measure\n2. Identify bottlenecks\n3. Optimize critical paths\n4. Measure improvements\n5. Document results"
        ),
        (
            "Security audit",
            "1. Review authentication\n2. Check authorization\n3. Validate input\n4. Audit dependencies\n5. Document findings"
        )
    ]
    
    for i, (task, solution) in enumerate(demonstrations, 1):
        await orchestrator.demonstrate(task, solution)
        print(f"  ✓ Demo {i}/{len(demonstrations)}: {task}")
    
    # Проверяем память
    print("\n🧠 Verifying memory...")
    stats = {
        "total_memories": len(orchestrator.memory.simple_memory.memories),
        "total_solutions": len(orchestrator.memory.simple_memory.task_solutions),
        "memory_types": {
            "simple": True,
            "task_centric": orchestrator.memory.memory_controller is not None,
            "mem0": orchestrator.memory.mem0_memory is not None,
            "vector": orchestrator.memory.vector_memory is not None
        }
    }
    
    print(f"\n📊 Memory Statistics:")
    print(f"  • Total memories: {stats['total_memories']}")
    print(f"  • Total solutions: {stats['total_solutions']}")
    print(f"  • Memory types:")
    for mem_type, available in stats['memory_types'].items():
        status = "✓" if available else "✗"
        print(f"    {status} {mem_type}")
    
    print("\n✅ Boss knowledge base initialized successfully!")
    print("\n🚀 Ready to delegate tasks through Codegen!")
    
    # Тестовый запрос
    print("\n🧪 Running test delegation...")
    try:
        test_result = await orchestrator.process_request(
            "Test delegation: Echo this message back",
            mode="boss"
        )
        print(f"  ✓ Test delegation created: Agent {test_result['agent_id']}")
        print(f"  • Used memory: {test_result['used_memory']}")
        if test_result.get('web_url'):
            print(f"  • Web URL: {test_result['web_url']}")
    except Exception as e:
        print(f"  ⚠️  Test delegation failed: {e}")
        print(f"  This is normal if Codegen API credentials are not configured")
    
    print("\n" + "="*60)
    print("Next steps:")
    print("1. Configure .env with your API keys")
    print("2. Run: docker-compose up -d")
    print("3. Test: curl http://localhost:8000/health")
    print("4. Use: curl -X POST http://localhost:8000/process \\")
    print("         -H 'Content-Type: application/json' \\")
    print("         -d '{\"task\": \"Your task here\"}'")
    print("="*60)

if __name__ == "__main__":
    asyncio.run(initialize())

