# ultimate_boss_with_memory.py
import asyncio
import os
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime
import json
import logging

# Autogen imports
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core.memory import (
    Memory,
    MemoryContent,
    MemoryMimeType,
    MemoryQueryResult,
)

# Task-Centric Memory
from autogen_ext.experimental.task_centric_memory import (
    MemoryController,
)

# Memory stores
from autogen_ext.memory.mem0 import Mem0Memory
from autogen_ext.memory.chromadb import (
    ChromaDBVectorMemory,
    ChromaDBVectorMemoryConfig,
    SentenceTransformerEmbeddingFunctionConfig
)

# Models
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Codegen client
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# === CODEGEN API CLIENT ===

class CodegenAPIClient:
    """Полный клиент для работы с Codegen API"""
    
    def __init__(self, org_id: str, token: str):
        self.org_id = org_id
        self.token = token
        self.base_url = "https://api.codegen.com/v1"
        self.headers = {"Authorization": f"Bearer {token}"}
    
    async def create_agent_run(
        self,
        prompt: str,
        repo_id: Optional[int] = None,
        parent_agent_run_id: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Создает агента в Codegen"""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/organizations/{self.org_id}/agent/run",
                headers=self.headers,
                json={
                    "prompt": prompt,
                    "repo_id": repo_id,
                    "parent_agent_run_id": parent_agent_run_id,
                    **kwargs
                },
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_agent_run(self, agent_run_id: int) -> Dict:
        """Получает статус агента"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/organizations/{self.org_id}/agent/run/{agent_run_id}",
                headers=self.headers,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    
    async def get_agent_logs(
        self,
        agent_run_id: int,
        skip: int = 0,
        limit: int = 100
    ) -> Dict:
        """Получает детальные логи агента"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/alpha/organizations/{self.org_id}/agent/run/{agent_run_id}/logs",
                headers=self.headers,
                params={"skip": skip, "limit": limit},
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()

# === SMART MEMORY SYSTEM ===

class BossMemorySystem:
    """Комплексная система памяти босса"""
    
    def __init__(self, model_client: OpenAIChatCompletionClient):
        # Task-Centric Memory Controller
        self.memory_controller = MemoryController(
            reset=False,
            client=model_client._client,
        )
        
        # Mem0 для долгосрочной памяти
        self.mem0_memory = Mem0Memory(
            is_cloud=False,
            config={"path": "./boss_mem0_storage"},
            user_id="boss",
            limit=10
        )
        
        # ChromaDB для векторного поиска
        self.vector_memory = ChromaDBVectorMemory(
            config=ChromaDBVectorMemoryConfig(
                collection_name="boss_memories",
                persist_directory="./boss_chroma_db",
                embedding_function=SentenceTransformerEmbeddingFunctionConfig(
                    model_name="all-MiniLM-L6-v2"
                )
            )
        )
        
        # Инициализация базовых знаний
        asyncio.create_task(self._initialize_base_knowledge())
    
    async def _initialize_base_knowledge(self):
        """Загружает базовые знания о делегировании"""
        
        # Паттерны успешного делегирования
        delegation_patterns = [
            ("bug_fix", "1. Reproduce issue\n2. Identify root cause\n3. Fix\n4. Test\n5. Verify"),
            ("feature", "1. Design\n2. Implement\n3. Test\n4. Document\n5. PR"),
            ("review", "Focus on: Security, Performance, Quality, Best practices"),
            ("multi_agent", "1. Break down\n2. Create sub-issues\n3. Assign agents\n4. Monitor")
        ]
        
        for task_type, pattern in delegation_patterns:
            await self.memory_controller.add_memo(
                task=f"How to handle {task_type} tasks",
                insight=pattern
            )
        
        # Codegen API знания
        codegen_insights = [
            ("Creating agents", "Use create_agent_run with detailed prompt"),
            ("Monitoring", "Check agent_run status and logs regularly"),
            ("Multi-agent", "Use parent_agent_run_id for hierarchical tasks"),
            ("Integrations", "GitHub, Slack, Linear, Jira available")
        ]
        
        for topic, insight in codegen_insights:
            await self.memory_controller.add_memo(
                task=f"Codegen: {topic}",
                insight=insight
            )
    
    async def remember_delegation(
        self,
        agent_id: str,
        task: str,
        result: Dict,
        success: bool
    ):
        """Запоминает результат делегирования"""
        
        # Task-centric memory
        if success:
            await self.memory_controller.add_task_solution_pair_to_memory(
                task=task,
                solution=json.dumps(result)[:500]
            )
        
        # Mem0 долгосрочная память
        await self.mem0_memory.add(
            MemoryContent(
                content=f"Delegation {agent_id}: {task} - Success: {success}",
                mime_type=MemoryMimeType.TEXT,
                metadata={
                    "agent_id": agent_id,
                    "success": success,
                    "timestamp": datetime.now().isoformat()
                }
            )
        )
        
        # Векторная память для поиска
        await self.vector_memory.add(
            MemoryContent(
                content=f"{task}\n{json.dumps(result)}",
                mime_type=MemoryMimeType.TEXT,
                metadata={"type": "delegation", "success": success}
            )
        )
    
    async def recall_best_approach(self, task: str) -> Optional[str]:
        """Вспоминает лучший подход для задачи"""
        
        # Сначала ищем в task-centric memory
        memos = await self.memory_controller.retrieve_relevant_memos(task)
        if memos:
            return memos[0].insight
        
        # Затем в векторной памяти
        results = await self.vector_memory.query(task)
        if results.results:
            return results.results[0].content
        
        return None
    
    async def learn_from_failure(self, task: str, error: str):
        """Учится на ошибках"""
        
        await self.memory_controller.add_memo(
            task=task,
            insight=f"Error encountered: {error}. Avoid this approach."
        )
        
        # Сохраняем в Mem0 для долгосрочного обучения
        await self.mem0_memory.add(
            MemoryContent(
                content=f"Failed approach for {task}: {error}",
                mime_type=MemoryMimeType.TEXT,
                metadata={"type": "failure", "task": task}
            )
        )

# === MEMORY-ENABLED BOSS AGENT ===

class UltimateBossWithMemory(AssistantAgent):
    """Босс-агент с полной памятью и делегированием через Codegen"""
    
    def __init__(
        self,
        codegen_client: CodegenAPIClient,
        memory_system: BossMemorySystem,
        model_client: OpenAIChatCompletionClient,
        **kwargs
    ):
        super().__init__(
            name="UltimateBoss",
            model_client=model_client,
            system_message="""You are the ULTIMATE BOSS AGENT with PERFECT MEMORY who delegates ALL tasks through Codegen.

KEY PRINCIPLES:
1. You NEVER write code yourself - ONLY delegate through Codegen API
2. You REMEMBER everything - every delegation, result, and learning
3. You LEARN from past experiences to optimize future delegations
4. You COORDINATE multiple agents for complex tasks

YOUR MEMORY CAPABILITIES:
- Task-centric memory for proven solutions
- Vector search for similar past tasks
- Long-term memory of all delegations
- Learning from failures and successes

DELEGATION STRATEGY:
1. Check memory for similar past tasks
2. Apply learned patterns and avoid past mistakes
3. Create optimized Codegen agents
4. Monitor and learn from results
5. Update memory with new insights

Always mention when using past experience: "Based on past experience with X..."
Never repeat past mistakes - always check what failed before.""",
            **kwargs
        )
        
        self.codegen = codegen_client
        self.memory_system = memory_system
        self.active_delegations = {}
    
    async def delegate_with_memory(
        self,
        task: str,
        task_type: str = "general"
    ) -> Dict:
        """Делегирует задачу, используя память"""
        
        # Проверяем память для похожих задач
        best_approach = await self.memory_system.recall_best_approach(task)
        
        # Формируем промпт с учетом памяти
        if best_approach:
            prompt = f"""Task: {task}

Based on past successful approaches:
{best_approach}

Apply these insights to complete the task efficiently."""
            logger.info(f"Using memory-informed approach for: {task}")
        else:
            prompt = f"Complete task: {task}"
            logger.info(f"No prior memory found for: {task}")
        
        # Создаем агента в Codegen
        result = await self.codegen.create_agent_run(prompt=prompt)
        agent_id = str(result["id"])
        
        # Сохраняем активное делегирование
        self.active_delegations[agent_id] = {
            "task": task,
            "type": task_type,
            "started_at": datetime.now(),
            "used_memory": bool(best_approach)
        }
        
        # Запускаем мониторинг
        asyncio.create_task(self._monitor_and_learn(agent_id))
        
        return {
            "agent_id": agent_id,
            "status": "delegated",
            "used_memory": bool(best_approach),
            "web_url": result.get("web_url")
        }
    
    async def _monitor_and_learn(self, agent_id: str):
        """Мониторит агента и учится на результатах"""
        
        max_checks = 60
        for _ in range(max_checks):
            try:
                # Получаем статус
                status = await self.codegen.get_agent_run(int(agent_id))
                
                if status["status"] in ["completed", "failed"]:
                    # Получаем детальные логи для анализа
                    logs = await self.codegen.get_agent_logs(int(agent_id))
                    
                    # Анализируем результат
                    success = status["status"] == "completed"
                    task = self.active_delegations[agent_id]["task"]
                    
                    # Запоминаем результат
                    await self.memory_system.remember_delegation(
                        agent_id=agent_id,
                        task=task,
                        result=status.get("result", {}),
                        success=success
                    )
                    
                    # Если неудача - учимся
                    if not success:
                        error = self._extract_error_from_logs(logs)
                        await self.memory_system.learn_from_failure(task, error)
                    
                    logger.info(f"Delegation {agent_id} completed. Success: {success}")
                    break
                
                await asyncio.sleep(10)
                
            except Exception as e:
                logger.error(f"Error monitoring {agent_id}: {e}")
                break
    
    def _extract_error_from_logs(self, logs: Dict) -> str:
        """Извлекает ошибки из логов"""
        errors = []
        for log in logs.get("logs", []):
            if log.get("message_type") == "ERROR":
                errors.append(log.get("observation", "Unknown error"))
        
        return " | ".join(errors) if errors else "Unknown error"
    
    async def teach_me(self, lesson: str):
        """Позволяет пользователю обучать босса"""
        
        # Извлекаем insight из урока
        await self.memory_system.memory_controller.add_memo(
            task="User teaching",
            insight=lesson
        )
        
        logger.info(f"Learned from user: {lesson}")

# === APPRENTICE BOSS (обучаемый босс) ===

class ApprenticeBoss:
    """Босс-ученик, который учится через практику"""
    
    def __init__(
        self,
        codegen_client: CodegenAPIClient,
        model_client: OpenAIChatCompletionClient
    ):
        self.codegen = codegen_client
        self.model_client = model_client
        
        # Memory system
        self.memory = BossMemorySystem(model_client)
        
        # Memory Controller для обучения
        self.memory_controller = self.memory.memory_controller
        
        # Boss agent
        self.boss = UltimateBossWithMemory(
            codegen_client=codegen_client,
            memory_system=self.memory,
            model_client=model_client,
            tools=[]  # Босс только делегирует!
        )
    
    async def train_on_task(
        self,
        task: str,
        expected_outcome: str
    ):
        """Тренирует босса на конкретной задаче"""
        
        # Обучение через добавление в память
        await self.memory_controller.add_task_solution_pair_to_memory(
            task=task,
            solution=expected_outcome
        )
        
        logger.info(f"Trained on task: {task}")
    
    async def demonstrate_solution(
        self,
        task: str,
        solution: str
    ):
        """Демонстрирует решение для обучения"""
        
        await self.memory_controller.add_task_solution_pair_to_memory(
            task=task,
            solution=solution
        )
        
        logger.info(f"Demonstrated solution for: {task}")
    
    async def process_with_learning(
        self,
        task: str,
        allow_retry: bool = True
    ) -> Dict:
        """Обрабатывает задачу с обучением"""
        
        # Делегируем через босса
        result = await self.boss.delegate_with_memory(task)
        
        # Если разрешены повторы - учимся на ошибках
        if allow_retry:
            agent_id = result["agent_id"]
            
            # Ждем результата
            for _ in range(30):
                status = await self.codegen.get_agent_run(int(agent_id))
                
                if status["status"] == "failed":
                    # Учимся на ошибке
                    logs = await self.codegen.get_agent_logs(int(agent_id))
                    error = self.boss._extract_error_from_logs(logs)
                    
                    # Добавляем в память как неудачный подход
                    await self.memory.learn_from_failure(task, error)
                    
                    # Пробуем снова с новым знанием
                    logger.info(f"Retrying with learned insights...")
                    result = await self.boss.delegate_with_memory(
                        task=f"{task}\n\nAvoid: {error}"
                    )
                    break
                
                elif status["status"] == "completed":
                    break
                
                await asyncio.sleep(10)
        
        return result

# === TEAM OF MEMORY-ENABLED AGENTS ===

class MemoryEnabledTeam:
    """Команда агентов с общей памятью"""
    
    def __init__(
        self,
        codegen_client: CodegenAPIClient,
        model_client: OpenAIChatCompletionClient
    ):
        # Общая память для команды
        self.shared_memory = BossMemorySystem(model_client)
        
        # Босс с памятью
        self.boss = UltimateBossWithMemory(
            codegen_client=codegen_client,
            memory_system=self.shared_memory,
            model_client=model_client
        )
        
        # Аналитик с памятью
        self.analyst = AssistantAgent(
            name="Analyst",
            model_client=model_client,
            system_message="You analyze tasks and provide insights based on memory."
        )
        
        # Координатор с памятью
        self.coordinator = AssistantAgent(
            name="Coordinator",
            model_client=model_client,
            system_message="You coordinate between agents using shared memory."
        )
        
        # Создаем команду
        self.team = RoundRobinGroupChat(
            participants=[self.boss, self.analyst, self.coordinator]
        )
    
    async def process_complex_task(self, task: str) -> Dict:
        """Обрабатывает сложную задачу командой"""
        
        # Анализируем задачу
        analysis_result = await self.analyst.run(
            task=f"Analyze this task and suggest approach: {task}"
        )
        
        # Координатор планирует
        plan_result = await self.coordinator.run(
            task=f"Create delegation plan based on analysis: {analysis_result.messages[-1].content}"
        )
        
        # Босс делегирует через Codegen
        delegations = []
        
        # Разбираем план на подзадачи (упрощенно)
        subtasks = plan_result.messages[-1].content.split("\n")[:5]
        
        for subtask in subtasks:
            if subtask.strip():
                delegation = await self.boss.delegate_with_memory(
                    task=subtask,
                    task_type="subtask"
                )
                delegations.append(delegation)
        
        return {
            "task": task,
            "analysis": analysis_result.messages[-1].content,
            "plan": plan_result.messages[-1].content,
            "delegations": delegations
        }

# === MAIN ORCHESTRATOR ===

class UltimateMemoryOrchestrator:
    """Главный оркестратор с полной памятью"""
    
    def __init__(
        self,
        codegen_org_id: str,
        codegen_token: str,
        openai_key: str
    ):
        # Model client
        self.model_client = OpenAIChatCompletionClient(
            model="gpt-4-turbo-preview",
            api_key=openai_key
        )
        
        # Codegen client
        self.codegen = CodegenAPIClient(codegen_org_id, codegen_token)
        
        # Apprentice Boss для обучения
        self.apprentice_boss = ApprenticeBoss(
            codegen_client=self.codegen,
            model_client=self.model_client
        )
        
        # Team для сложных задач
        self.team = MemoryEnabledTeam(
            codegen_client=self.codegen,
            model_client=self.model_client
        )
        
        # Console UI
        self.console = Console()
    
    async def process_request(
        self,
        request: str,
        mode: str = "auto"
    ) -> Dict:
        """Обрабатывает запрос с автоматическим выбором стратегии"""
        
        if mode == "auto":
            # Определяем сложность
            if "complex" in request.lower() or "multi" in request.lower():
                mode = "team"
            else:
                mode = "boss"
        
        if mode == "boss":
            # Простое делегирование через босса
            result = await self.apprentice_boss.boss.delegate_with_memory(request)
            
        elif mode == "team":
            # Сложная задача через команду
            result = await self.team.process_complex_task(request)
            
        elif mode == "learn":
            # Обучение через практику
            result = await self.apprentice_boss.process_with_learning(
                request,
                allow_retry=True
            )
        
        return result
    
    async def teach(self, lesson: str):
        """Обучает систему новому знанию"""
        await self.apprentice_boss.boss.teach_me(lesson)
        return {"status": "learned", "lesson": lesson}
    
    async def demonstrate(self, task: str, solution: str):
        """Демонстрирует решение для обучения"""
        await self.apprentice_boss.demonstrate_solution(task, solution)
        return {"status": "demonstrated", "task": task}

# === API SERVER ===

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Ultimate Boss with Memory API")

orchestrator = None

@app.on_event("startup")
async def startup():
    global orchestrator
    orchestrator = UltimateMemoryOrchestrator(
        codegen_org_id=os.getenv("CODEGEN_ORG_ID"),
        codegen_token=os.getenv("CODEGEN_API_TOKEN"),
        openai_key=os.getenv("OPENAI_API_KEY")
    )

class TaskRequest(BaseModel):
    task: str
    mode: str = "auto"  # auto, boss, team, learn

class TeachRequest(BaseModel):
    lesson: str

class DemonstrateRequest(BaseModel):
    task: str
    solution: str

@app.post("/process")
async def process_task(request: TaskRequest):
    """Обрабатывает задачу с памятью"""
    result = await orchestrator.process_request(
        request.task,
        request.mode
    )
    return result

@app.post("/teach")
async def teach_boss(request: TeachRequest):
    """Обучает босса новому знанию"""
    result = await orchestrator.teach(request.lesson)
    return result

@app.post("/demonstrate")
async def demonstrate_solution(request: DemonstrateRequest):
    """Демонстрирует решение"""
    result = await orchestrator.demonstrate(
        request.task,
        request.solution
    )
    return result

@app.get("/memory/search")
async def search_memory(query: str):
    """Ищет в памяти босса"""
    mem0_results = await orchestrator.apprentice_boss.memory.mem0_memory.query(query)
    vector_results = await orchestrator.apprentice_boss.memory.vector_memory.query(query)
    
    return {
        "mem0": [r.content for r in mem0_results.results],
        "vector": [r.content for r in vector_results.results]
    }

@app.get("/memory/stats")
async def memory_stats():
    """Статистика памяти"""
    # Получаем все воспоминания для статистики
    all_memories = await orchestrator.apprentice_boss.memory.mem0_memory.query("")
    
    return {
        "total_memories": len(all_memories.results),
        "active_delegations": len(orchestrator.apprentice_boss.boss.active_delegations),
        "memory_types": {
            "task_solutions": sum(1 for m in all_memories.results if "task" in str(m.metadata)),
            "failures": sum(1 for m in all_memories.results if "failure" in str(m.metadata)),
            "delegations": sum(1 for m in all_memories.results if "delegation" in str(m.metadata))
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
