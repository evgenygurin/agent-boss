# 💡 Ultimate Boss Agent - Examples

Коллекция практических примеров использования Ultimate Boss Agent.

## 📋 Table of Contents

- [Basic Delegation](#basic-delegation)
- [Team Coordination](#team-coordination)
- [Learning & Teaching](#learning--teaching)
- [Memory Management](#memory-management)
- [Real-World Scenarios](#real-world-scenarios)
- [Advanced Usage](#advanced-usage)

## Basic Delegation

### Example 1: Simple Bug Fix

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Fix the authentication bug where users cannot log in with special characters in password",
    "mode": "boss"
  }'
```

**Response:**
```json
{
  "agent_id": "12345",
  "status": "delegated",
  "used_memory": true,
  "web_url": "https://app.codegen.com/agent/12345"
}
```

### Example 2: Feature Implementation

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Add dark mode toggle to user settings page with persistent storage",
    "mode": "auto"
  }'
```

### Example 3: Code Refactoring

```python
import asyncio
import httpx

async def refactor_code():
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": "Refactor authentication service to use dependency injection pattern",
                "mode": "boss"
            }
        )
        result = response.json()
        print(f"✓ Refactoring delegated to agent {result['agent_id']}")
        print(f"  Memory used: {result['used_memory']}")

asyncio.run(refactor_code())
```

## Team Coordination

### Example 4: Complex Multi-Step Task

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Implement complete payment system: Stripe integration, webhook handling, transaction logging, error recovery, and admin dashboard",
    "mode": "team"
  }'
```

**How it works:**
1. **Analyst** analyzes the task and breaks it down
2. **Coordinator** creates execution plan
3. **Boss** delegates through Codegen API
4. All agents share memory for coordination

### Example 5: Microservices Migration

```python
import asyncio
import httpx

async def migrate_to_microservices():
    async with httpx.AsyncClient(timeout=120.0) as client:
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": """Migrate monolithic application to microservices:
                1. Extract user service
                2. Extract payment service
                3. Extract notification service
                4. Set up API gateway
                5. Implement service discovery
                6. Add monitoring and logging
                """,
                "mode": "team"
            }
        )
        
        result = response.json()
        
        print("🚀 Migration started!")
        print(f"   Main delegation: {result['delegation']['agent_id']}")
        print(f"   Team: {result['team']}")

asyncio.run(migrate_to_microservices())
```

## Learning & Teaching

### Example 6: Teaching Best Practices

```python
import asyncio
import httpx

async def teach_best_practices():
    lessons = [
        "Always write unit tests before implementing features (TDD)",
        "Use meaningful variable names that explain intent",
        "Keep functions small and focused on single responsibility",
        "Document public APIs with clear examples",
        "Handle errors gracefully with proper logging",
        "Use environment variables for configuration",
        "Implement proper input validation",
        "Follow security best practices (OWASP Top 10)",
        "Write clear commit messages with issue references",
        "Review code for performance implications"
    ]
    
    async with httpx.AsyncClient() as client:
        for i, lesson in enumerate(lessons, 1):
            await client.post(
                "http://localhost:8000/teach",
                json={"lesson": lesson}
            )
            print(f"✓ Lesson {i}/{len(lessons)}: {lesson[:50]}...")
    
    print("\n✅ Boss trained with best practices!")

asyncio.run(teach_best_practices())
```

### Example 7: Demonstrating Solutions

```python
import asyncio
import httpx

async def demonstrate_workflows():
    workflows = [
        {
            "task": "CI/CD Pipeline Setup",
            "solution": """
1. Configure GitHub Actions workflow
2. Add build and test jobs
3. Implement code quality checks
4. Add deployment job with approval
5. Configure environment secrets
6. Set up monitoring and alerts
            """
        },
        {
            "task": "Database Migration",
            "solution": """
1. Create migration script
2. Test migration on staging
3. Backup production database
4. Run migration with rollback plan
5. Verify data integrity
6. Monitor performance
            """
        },
        {
            "task": "Security Audit",
            "solution": """
1. Run automated security scanners
2. Review authentication mechanisms
3. Check authorization logic
4. Validate input sanitization
5. Audit dependency vulnerabilities
6. Review logging and monitoring
7. Document findings and fixes
            """
        }
    ]
    
    async with httpx.AsyncClient() as client:
        for workflow in workflows:
            await client.post(
                "http://localhost:8000/demonstrate",
                json=workflow
            )
            print(f"✓ Demonstrated: {workflow['task']}")
    
    print("\n✅ Workflows demonstrated!")

asyncio.run(demonstrate_workflows())
```

### Example 8: Learning Mode with Retry

```bash
curl -X POST http://localhost:8000/process \
  -H "Content-Type: application/json" \
  -d '{
    "task": "Implement rate limiting middleware with Redis backend",
    "mode": "learn"
  }'
```

**How it works:**
1. Boss delegates task to Codegen
2. Monitors execution
3. If it fails, learns from the error
4. Retries with improved approach
5. Saves successful pattern to memory

## Memory Management

### Example 9: Searching Memory

```python
import asyncio
import httpx

async def search_for_solutions():
    queries = [
        "authentication",
        "deployment",
        "performance optimization",
        "security audit"
    ]
    
    async with httpx.AsyncClient() as client:
        for query in queries:
            response = await client.get(
                "http://localhost:8000/memory/search",
                params={"query": query}
            )
            results = response.json()
            
            print(f"\n🔍 Search: '{query}'")
            print(f"   Found {len(results['results'])} memories")
            
            for i, memory in enumerate(results['results'][:3], 1):
                content = memory['content'][:80]
                print(f"   {i}. {content}...")

asyncio.run(search_for_solutions())
```

### Example 10: Memory Statistics

```python
import asyncio
import httpx
import json

async def analyze_memory():
    async with httpx.AsyncClient() as client:
        response = await client.get("http://localhost:8000/memory/stats")
        stats = response.json()
        
        print("📊 Memory Analysis")
        print("="*50)
        print(f"Total memories: {stats['total_memories']}")
        print(f"Total solutions: {stats['total_solutions']}")
        print(f"Active delegations: {stats['active_delegations']}")
        
        print("\n🧠 Memory Types:")
        for mem_type, available in stats['memory_types'].items():
            status = "✓" if available else "✗"
            print(f"  {status} {mem_type}")

asyncio.run(analyze_memory())
```

## Real-World Scenarios

### Example 11: Bug Triage and Fix

```python
import asyncio
import httpx

async def bug_triage_workflow():
    """Complete workflow: teach → demonstrate → delegate"""
    
    async with httpx.AsyncClient() as client:
        # 1. Teach bug handling approach
        await client.post(
            "http://localhost:8000/teach",
            json={
                "lesson": "For bugs: reproduce, identify root cause, fix, test, verify"
            }
        )
        
        # 2. Demonstrate bug fix workflow
        await client.post(
            "http://localhost:8000/demonstrate",
            json={
                "task": "Bug fix workflow",
                "solution": "1. Reproduce\n2. Write failing test\n3. Fix\n4. Verify\n5. Check regressions"
            }
        )
        
        # 3. Delegate actual bug fix
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": "Fix bug: users getting 500 error when uploading files > 10MB",
                "mode": "boss"
            }
        )
        
        result = response.json()
        print(f"✓ Bug fix delegated: Agent {result['agent_id']}")
        print(f"  Used proven workflow: {result['used_memory']}")

asyncio.run(bug_triage_workflow())
```

### Example 12: Feature Development Lifecycle

```python
import asyncio
import httpx

async def feature_lifecycle():
    """Complete feature development with memory"""
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        # Phase 1: Planning
        print("📋 Phase 1: Planning")
        await client.post(
            "http://localhost:8000/teach",
            json={"lesson": "Break features into small, testable increments"}
        )
        
        # Phase 2: Design
        print("🎨 Phase 2: Design")
        await client.post(
            "http://localhost:8000/demonstrate",
            json={
                "task": "Feature design",
                "solution": "1. Requirements\n2. Architecture\n3. API design\n4. Data model\n5. UI mockups"
            }
        )
        
        # Phase 3: Implementation
        print("⚙️  Phase 3: Implementation")
        impl_response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": """Implement user profile feature:
                - Profile page with avatar upload
                - Edit profile form with validation
                - Privacy settings
                - Activity history
                - API endpoints with tests
                """,
                "mode": "team"
            }
        )
        
        result = impl_response.json()
        print(f"✓ Implementation started: {result['delegation']['agent_id']}")
        
        # Phase 4: Testing (teach for future)
        print("🧪 Phase 4: Testing approach saved")
        await client.post(
            "http://localhost:8000/teach",
            json={"lesson": "Test user flows, edge cases, and error scenarios"}
        )
        
        print("\n✅ Complete feature lifecycle initiated!")

asyncio.run(feature_lifecycle())
```

### Example 13: Production Incident Response

```python
import asyncio
import httpx

async def incident_response():
    """Automated incident response workflow"""
    
    async with httpx.AsyncClient() as client:
        # 1. Teach incident response protocol
        await client.post(
            "http://localhost:8000/teach",
            json={
                "lesson": "Incidents: assess impact, mitigate, fix root cause, post-mortem"
            }
        )
        
        # 2. Demonstrate mitigation steps
        await client.post(
            "http://localhost:8000/demonstrate",
            json={
                "task": "Production incident response",
                "solution": """
1. Assess impact and severity
2. Notify stakeholders
3. Implement immediate mitigation
4. Identify root cause
5. Deploy permanent fix
6. Write post-mortem
7. Implement preventive measures
                """
            }
        )
        
        # 3. Delegate incident handling
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": """Production incident: Database connection pool exhausted.
                Users experiencing slow response times.
                Mitigate immediately and fix root cause.
                """,
                "mode": "learn"  # Learn from incident handling
            }
        )
        
        result = response.json()
        print(f"🚨 Incident response initiated: Agent {result['agent_id']}")
        print(f"   Using proven protocols: {result['used_memory']}")

asyncio.run(incident_response())
```

## Advanced Usage

### Example 14: Batch Delegation

```python
import asyncio
import httpx

async def batch_delegate():
    """Delegate multiple related tasks"""
    
    tasks = [
        "Add unit tests for authentication service",
        "Add integration tests for payment service",
        "Add E2E tests for checkout flow",
        "Set up test coverage reporting",
        "Configure CI to run tests automatically"
    ]
    
    async with httpx.AsyncClient() as client:
        delegations = []
        
        for task in tasks:
            response = await client.post(
                "http://localhost:8000/process",
                json={"task": task, "mode": "boss"}
            )
            result = response.json()
            delegations.append({
                "task": task,
                "agent_id": result['agent_id'],
                "used_memory": result['used_memory']
            })
        
        print(f"✅ Delegated {len(delegations)} tasks:")
        for d in delegations:
            memory_indicator = "🧠" if d['used_memory'] else "🆕"
            print(f"   {memory_indicator} Agent {d['agent_id']}: {d['task'][:50]}...")

asyncio.run(batch_delegate())
```

### Example 15: Progressive Enhancement

```python
import asyncio
import httpx
import time

async def progressive_enhancement():
    """Gradually improve with learning"""
    
    async with httpx.AsyncClient(timeout=180.0) as client:
        iterations = [
            ("Basic implementation", "boss"),
            ("Add error handling", "learn"),
            ("Optimize performance", "learn"),
            ("Add monitoring", "learn"),
            ("Production hardening", "team")
        ]
        
        for i, (description, mode) in enumerate(iterations, 1):
            print(f"\n🔄 Iteration {i}: {description}")
            
            response = await client.post(
                "http://localhost:8000/process",
                json={
                    "task": f"User notification system: {description}",
                    "mode": mode
                }
            )
            
            result = response.json()
            print(f"   Agent: {result.get('agent_id', result.get('delegation', {}).get('agent_id'))}")
            
            # Brief pause between iterations
            await asyncio.sleep(2)
        
        print("\n✅ Progressive enhancement complete!")

asyncio.run(progressive_enhancement())
```

### Example 16: Memory-Driven Development

```python
import asyncio
import httpx

async def memory_driven_dev():
    """Use memory to guide development"""
    
    async with httpx.AsyncClient() as client:
        # 1. Check what we know about similar tasks
        search = await client.get(
            "http://localhost:8000/memory/search",
            params={"query": "API implementation"}
        )
        
        previous_knowledge = search.json()
        print(f"🧠 Found {len(previous_knowledge['results'])} relevant memories")
        
        # 2. Delegate with memory context
        response = await client.post(
            "http://localhost:8000/process",
            json={
                "task": "Implement REST API for product catalog with pagination, filtering, and search",
                "mode": "boss"  # Boss will use found memories
            }
        )
        
        result = response.json()
        
        if result['used_memory']:
            print("✓ Used past experience to optimize delegation")
        else:
            print("✓ New pattern - will learn from this")
        
        # 3. Save new learnings
        await client.post(
            "http://localhost:8000/teach",
            json={
                "lesson": "REST APIs should include: pagination, filtering, search, sorting, and proper HTTP status codes"
            }
        )
        
        print("✅ Memory-driven development cycle complete")

asyncio.run(memory_driven_dev())
```

## 📊 Monitoring Examples

### Example 17: Dashboard Data

```python
import asyncio
import httpx
from datetime import datetime

async def dashboard():
    """Create real-time dashboard"""
    
    async with httpx.AsyncClient() as client:
        while True:
            # Get stats
            stats_response = await client.get("http://localhost:8000/memory/stats")
            stats = stats_response.json()
            
            # Get health
            health_response = await client.get("http://localhost:8000/health")
            health = health_response.json()
            
            # Display
            print("\033[2J\033[H")  # Clear screen
            print(f"🤖 Ultimate Boss Dashboard - {datetime.now().strftime('%H:%M:%S')}")
            print("="*60)
            
            print(f"\n📊 Statistics:")
            print(f"   Memories: {stats['total_memories']}")
            print(f"   Solutions: {stats['total_solutions']}")
            print(f"   Active: {stats['active_delegations']}")
            
            print(f"\n💚 Health:")
            for component, status in health['components'].items():
                indicator = "✓" if status else "✗"
                print(f"   {indicator} {component}")
            
            print(f"\n🧠 Memory Systems:")
            for mem_type, available in stats['memory_types'].items():
                indicator = "✓" if available else "✗"
                print(f"   {indicator} {mem_type}")
            
            await asyncio.sleep(5)

# Run with: asyncio.run(dashboard())
```

---

## 🎓 Learning Path

Рекомендуемый порядок изучения примеров:

1. **Beginners:** Examples 1-3 (Basic delegation)
2. **Intermediate:** Examples 6-10 (Learning & Memory)
3. **Advanced:** Examples 11-13 (Real-world scenarios)
4. **Expert:** Examples 14-17 (Advanced patterns)

---

Made with ❤️ by [Evgeny Gurin](https://github.com/evgenygurin)

