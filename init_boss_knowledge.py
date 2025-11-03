# init_boss_knowledge.py
import asyncio
import os
from ultimate_boss_with_memory import UltimateMemoryOrchestrator

async def initialize():
    """Инициализация базовых знаний босса"""
    
    orchestrator = UltimateMemoryOrchestrator(
        codegen_org_id=os.getenv("CODEGEN_ORG_ID"),
        codegen_token=os.getenv("CODEGEN_API_TOKEN"),
        openai_key=os.getenv("OPENAI_API_KEY")
    )
    
    print("🧠 Initializing Boss Knowledge Base...")
    
    # Обучаем базовым паттернам
    lessons = [
        "Always check CI/CD status before merging PRs",
        "Use Linear sub-issues for complex tasks",
        "Monitor Sentry for production errors",
        "Create comprehensive tests for all features",
        "Document all API changes",
        "Use semantic commit messages",
        "Review code for security vulnerabilities",
        "Ensure proper error handling in all functions",
        "Write clean, maintainable code following best practices",
        "Test edge cases and error conditions"
    ]
    
    print("\n📚 Teaching lessons...")
    for i, lesson in enumerate(lessons, 1):
        await orchestrator.teach(lesson)
        print(f"  ✓ Lesson {i}/{len(lessons)}: {lesson[:50]}...")
    
    # Демонстрируем успешные решения
    demonstrations = [
        (
            "Fix failing tests",
            "1. Run tests locally to reproduce\n2. Identify failing test and root cause\n3. Fix the code\n4. Verify fix with local test run\n5. Commit with descriptive message"
        ),
        (
            "Deploy to production",
            "1. Verify all tests pass on staging\n2. Run smoke tests\n3. Deploy using CI/CD pipeline\n4. Monitor logs and metrics\n5. Rollback if issues detected"
        ),
        (
            "Code review process",
            "1. Check code logic and correctness\n2. Review for security vulnerabilities\n3. Verify test coverage\n4. Check performance implications\n5. Ensure documentation is updated"
        ),
        (
            "Debug production issue",
            "1. Check error logs in monitoring system\n2. Reproduce issue in staging\n3. Identify root cause\n4. Implement fix with tests\n5. Deploy and verify resolution"
        ),
        (
            "Implement new feature",
            "1. Design feature architecture\n2. Break down into subtasks\n3. Implement with TDD approach\n4. Write documentation\n5. Create PR with comprehensive description"
        )
    ]
    
    print("\n🎯 Demonstrating solutions...")
    for i, (task, solution) in enumerate(demonstrations, 1):
        await orchestrator.demonstrate(task, solution)
        print(f"  ✓ Demo {i}/{len(demonstrations)}: {task}")
    
    print("\n✅ Boss knowledge base initialized successfully!")
    print("\n📊 Summary:")
    print(f"  - {len(lessons)} lessons taught")
    print(f"  - {len(demonstrations)} solutions demonstrated")
    print(f"  - Boss is ready to delegate tasks through Codegen!")

if __name__ == "__main__":
    asyncio.run(initialize())
